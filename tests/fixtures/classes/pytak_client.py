import asyncio
import xml.etree.ElementTree as ET
from configparser import ConfigParser, SectionProxy

import pytak

class PytakWorker(pytak.QueueWorker):
    def __init__(self, queue: asyncio.Queue, config: dict, message: ET.Element) -> None:
        super().__init__(queue, config)
        self._message = message

    async def handle_data(self, data: ET.Element) -> None:
        cot_string: str = ET.tostring(data).decode()
        await self.put_queue(cot_string)

    async def run(self):
        await self.handle_data(self._message)

class SendWorker(pytak.QueueWorker):
    def __init__(self, queue: asyncio.Queue, config: dict, message: ET.Element) -> None:
        super().__init__(queue, config)
        self._message = message

    async def handle_data(self, data: bytes) -> None:
        cot_string: str = ET.tostring(data)
        await self.put_queue(cot_string)

    async def run(self):
        self.handle_data(self._message)


class ReceiveWorker(pytak.RXWorker):
    async def handle_data(self) -> None:
        cot: ET.Element = self.queue.get()

    async def run(self):

        await self.handle_data()

class PytakClient:
    def __init__(self, config = None) -> None:
        self._config = config

    async def create(self, config = None) -> None:
        if config is None:
            self._config = self._setup_config()

        cli_tool = pytak.CLITool(self._config)
        await cli_tool.setup()
        await cli_tool.run()

        self._cli_tool = cli_tool

    async def send_message(self, message: ET.Element):
        self._cli_tool.add_task(SendWorker(self._cli_tool.tx_queue, self._config, message))

    async def get_latest_message(self):
        try:
            return await self._cli_tool.rx_queue.get()
        except asyncio.QueueEmpty:
            return ''
    
    def _setup_config(self) -> SectionProxy:
        config = ConfigParser()
        config['fts'] = {
            'COT_URL': 'tcp://127.0.0.1:8087',
            'CALLSIGN': 'PYTEST',
        }

        return config['fts']