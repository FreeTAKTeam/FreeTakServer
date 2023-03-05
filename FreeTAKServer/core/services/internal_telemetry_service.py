import zmq
import json

ERROR = 1
INFO = 2
DEBUG = 3

class InternalTelemetryService:
    """a service responsible for aggregating and exposing the log data of all components"""

    def __init__(self, max_queue_length: int, error_log_path: str, info_log_path: str, debug_log_path: str, port: int, host: str):
        """
        Args:
            max_queue_length (int): the maximum length any log queue may reach until
                its contents are archived in the log file on disk
            error_log_path (str): the path to the file where the overflow of the error log can be stored
            info_log_path (str): the path to the file where the overflow of the info log can be stored
            debug_log_path (str): the path to the file where the overflow of the debug log can be stored
            host (str): the host on which to listen for new host publisher collection
            port (int): the port on which to listen for new log publisher collection
        """
        # the path to save error logs once the error queue is overfilled
        self.error_log_path = error_log_path
        # the queue of error level log entries
        self.error_queue = []

        # the path to save info logs once the info queue is overfilled
        self.info_log_path = info_log_path
        # the queue of info level log entries
        self.info_queue = []

        # the path to save debug logs once the debug queue is overfilled
        self.debug_log_path = debug_log_path
        # the queue of debug level log entries
        self.debug_queue = []

        # the maximum number of items in any given queue before it
        # begins to be overloaded into the filesystem
        self.max_queue_length = max_queue_length

        # the host on which to listen for log publishers
        self.host = host
        # the port on which to listen for log publishers
        self.port = port

    def get_errors(self)->list:
        """return all errors in the error queue"""
        return self.error_queue

    def get_info(self) -> list:
        """return all info log entries in the info queue"""
        return self.info_queue

    def get_debug(self) -> list:
        """return all debug log entries in the debug log queue"""
        return self.debug_queue

    def save_log_entry(self, log_entry: dict, log_path: str):
        """save a given entry to a given path"""
        fp = open(log_path, mode="a")
        json.dump(log_entry, fp)
        fp.close()

    def add_log_to_queue(self, log_entry: dict, log_path: str, queue: list):
        """add a given log entry to the specified queue, displacing the
        last entry in the queue if the queue has reached it's limit"""
        if len(queue)==self.max_queue_length:
            self.save_log_entry(queue.pop(0), log_path)
        queue.append(log_entry)

    def add_log(self, log_entry: dict):
        """add a log entry to one of the queues"""
        if log_entry["level"] == DEBUG:
            self.add_log_to_queue(log_entry=log_entry, log_path=self.debug_log_path, queue=self.debug_queue)
        elif log_entry["level"] == INFO:
            self.add_log_to_queue(log_entry=log_entry, log_path=self.info_log_path, queue=self.info_queue)
        elif log_entry["level"] == ERROR:
            self.add_log_to_queue(log_entry=log_entry, log_path=self.error_log_path, queue=self.error_queue)

    def instantiate_sockets(self):
        """instantiate the required subscriber port"""
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.bind(f"tcp://{self.host}:{self.port}")
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")

    def main(self):
        """main loop for the reception and processing of log messages
        """
        self.instantiate_sockets()
        while True:
            try:
                # receive the data from the socket, load it as a dictionary, and save it to its queue
                self.add_log(
                    json.loads(self.socket.recv_multipart()[0].decode())
                )
            except Exception as e:
                print(e)
