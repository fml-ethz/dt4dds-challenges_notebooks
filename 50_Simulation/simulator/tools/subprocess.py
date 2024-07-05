import psutil
import pathlib
import dataclasses
import time

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def kill_process_family(process):
    processes = process.children(recursive=True)
    processes.append(process)
    for p in processes:
        try:
            p.kill()
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(processes, timeout=10)
    if alive:
        logger.warning(f"Some processes were not killed within timeout: [{','.join([str(p) for p in alive])}]")


@dataclasses.dataclass
class SubProcess():
    """  """

    command_args: list                      # list of arguments to pass to the subprocess
    monitor_interval: float = 0.2           # interval in seconds to collect subprocess resource data
    process_log_file: pathlib.Path = None   # path to the file to which the subprocess output will be written
    timeout: float = 2*60*60.0              # time in seconds until the subprocess is assumed to be dead and is killed

    process = None
    return_code = None
    start_time = None
    end_time = None
    resource_stats = None

    duration = property(lambda self: self.end_time - self.start_time)

    @property
    def metadata(self):
        """ Returns a dict with the metadata of the finished subprocess. """
        return {
            'return_code': self.return_code,
            'duration': self.duration,
        }


    def __post_init__(self):

        # create the log file handler if enabled
        if self.process_log_file is not None:
            self.process_log_file.parent.mkdir(parents=True, exist_ok=True)
            stdout = self.process_log_file.open('w')
        else:
            stdout = None

        # start the process
        self.start_time = time.time()
        logger.debug(f"Starting subprocess: {' '.join(self.command_args)}")
        self.process = psutil.Popen(self.command_args, stdout=stdout, stderr=stdout)

        # wait for the process to finish, while monitoring time-out
        while self.process.poll() is None:
            if time.time() - self.start_time > self.timeout:
                logger.critical(f"Subprocess timed out after {self.timeout} seconds, killing it.")
                kill_process_family(self.process)
                break

            # sleep for a bit
            time.sleep(0.05)

        # assign return code and end time
        self.return_code = self.process.wait()
        self.end_time = time.time()
