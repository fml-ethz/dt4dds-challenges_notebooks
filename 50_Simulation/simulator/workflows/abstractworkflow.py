import time
import pathlib
import dataclasses

from ..tools import Step

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclasses.dataclass
class AbstractWorkflow(Step):
    """ Abstract class for workflows. To be overridden by actual workflow implementations as a subclass. """

    # 
    # public methods
    # 

    def run(self, sequence_file: pathlib.Path, output_dir: pathlib.Path, **kwargs):
        """ Use the sequences in the design file and simulate the workflow, depositing sequencing data in the output directory. Returns the metadata of the process. """
        
        logger.info(f"Running {self} on {sequence_file}, outputting to {output_dir}.")
        start = time.time()

        try:
            process = self._run_workflow(pathlib.Path(sequence_file), pathlib.Path(output_dir), **kwargs)
            return process.metadata
        except Exception as e:
            logger.error(f"Workflow failed with {e}")
            raise e
        finally:
            logger.info(f"Workflow {self} took {time.time()-start:.1f} seconds")


    # 
    # override these methods in the subclass
    # 

    def _run_workflow(self, sequence_file: pathlib.Path, output_dir: pathlib.Path, **kwargs):
        """ To be override by the subclass """
        raise NotImplementedError("_run_workflow() not implemented")