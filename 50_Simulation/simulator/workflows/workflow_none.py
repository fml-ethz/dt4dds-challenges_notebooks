import dataclasses
import pathlib

from .abstractworkflow import AbstractWorkflow
from ..tools import SubProcess

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclasses.dataclass
class NoWorkflow(AbstractWorkflow):
    """
    Simple conversion of the design file to sequencing files.

    After initialization, the workflow can be used to run a simulation by calling run().    
    """

    command_path: str = dataclasses.field(default_factory = lambda: str(pathlib.Path(__file__).parent.absolute() / 'workflow_none.sh'))


    def _run_workflow(self, sequence_file: pathlib.Path, output_dir: pathlib.Path, **kwargs):

        cmd = [self.command_path]

        # add required arguments
        cmd.append(str(sequence_file.resolve()))
        cmd.append(str(output_dir.resolve()))

        return SubProcess(cmd, **kwargs)