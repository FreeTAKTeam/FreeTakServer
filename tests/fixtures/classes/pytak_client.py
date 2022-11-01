import asyncio
from typing import Union
import xml.etree.ElementTree as ET
from configparser import ConfigParser, SectionProxy

import pytak

class SendWorker(pytak.QueueWorker):
    def __init__(self, queue: asyncio.Queue, config: dict, message: ET.Element) -> None:
        super().__init__(queue, config)
        self._message = message

    async def handle_data(self, data: bytes) -> None:
        cot_string: str = ET.tostring(data)
        await self.put_queue(cot_string)

    async def run(self):
        await self.handle_data(self._message)

class ReceiveWorker(pytak.QueueWorker):
    def __init__(self, queue: asyncio.Queue, config: dict) -> None:
        super().__init__(queue, config)

    async def run(self):
        return await self.queue.get()


class FTSCLITool(pytak.CLITool):
    def __init__(self, config: ConfigParser, tx_queue: Union[asyncio.Queue, None] = None, rx_queue: Union[asyncio.Queue, None] = None) -> None:
        super().__init__(config, tx_queue, rx_queue)
        self.tasks_to_complete = set()
        self.running_c_tasks = set()

    def add_c_task(self, task):
        self.tasks_to_complete.add(task)

    def run_c_task(self, task):
        self.running_c_tasks.add(asyncio.ensure_future(task.run()))

    def run_c_tasks(self, tasks=None):
        tasks = tasks or self.tasks_to_complete
        for task in tasks:
            self.run_c_task(task)

    async def run(self):
        """Runs this Thread and its associated coroutine tasks."""
        self._logger.info("Run: %s", self.__class__)

        # await self.hello_event()
        self.run_tasks()
        self.run_c_tasks()

        done, _ = await asyncio.wait(
            self.running_c_tasks, return_when=asyncio.ALL_COMPLETED
        )

        results = []

        for task in done:
            result = task.result()

            if result is not None:
                results.append(result)

        # Close TX and RX workers aka connection to Server
        for task in self.running_tasks:
            task.cancel()

        return results

class PytakClient:
    def __init__(self, config = None) -> None:
        self._config = config

    def _setup_config(self) -> SectionProxy:
        """Create config if a custom one is not passed

        :return: Configuration
        :rtype: SectionProxy
        """
        config = ConfigParser()
        config['fts'] = {
            'COT_URL': 'tcp://127.0.0.1:8087',
            'CALLSIGN': 'FTS_PYTAK',
        }

        return config['fts']


    async def create_and_send_message(self, message: ET.Element, config: ConfigParser = None):
        # Setup cli tool
        if config is None:
            self._config = self._setup_config()

        cli_tool = FTSCLITool(self._config)
        await cli_tool.setup()

        # Send message to the server
        cli_tool.add_c_task(SendWorker(cli_tool.tx_queue, self._config, message))

        # Read latest message from server
        cli_tool.add_c_task(ReceiveWorker(cli_tool.rx_queue, self._config))

        return await cli_tool.run()
