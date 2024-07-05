import time
import tempfile
import pathlib
import shutil
import dataclasses

from ..tools import logs, FileDataFrame

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



@dataclasses.dataclass
class AbstractPipeline():

    # file-related settings
    input_file: pathlib.Path            # path to the input file
    iteration: int = None               # iteration number, if applicable
    output_folder: pathlib.Path = None  # path to the output folder, if None, a temporary folder will be used and deleted afterwards
    delete_output_folder: bool = False  # whether to delete the output folder after running the pipeline
    process_timeout: int = 60*60*1      # timeout for each process in seconds

    # log files
    log_file_name = 'pipeline.log'
    process_log_file_suffix = '.log'

    # output-related settings
    results_file_name: str = 'results.csv'
    metadata_file_name: str = 'metadata.csv'

    # properties
    _input_filepath = property(lambda self: self.output_folder.resolve() / self.input_file.name)


    def __repr__(self):
        return f"{self.__class__.__name__}({self.input_file.name})"


    @classmethod
    def factory(cls, **kwargs):
        raise NotImplementedError
    

    @property
    def _pipeline(self):
        raise NotImplementedError


    def run(self):
        # check that the input file exists
        self.input_file = pathlib.Path(self.input_file)
        if not self.input_file.exists():
            raise FileNotFoundError(f'Input file {self.input_file} does not exist.')

        # check that the output folder does not exist yet
        if self.output_folder:
            self.output_folder = pathlib.Path(self.output_folder)
            if self.output_folder and self.output_folder.exists():
                raise FileExistsError(f'Output folder {self.output_folder} already exists.')
        else:
            self.output_folder = pathlib.Path(tempfile.mkdtemp())
            self.delete_output_folder = True

        # initialize the dataframes for the results
        self.results = FileDataFrame(self.output_folder / self.results_file_name)
        self.metadata = FileDataFrame(self.output_folder / self.metadata_file_name)

        # set up the output folder and the overall logger
        self.output_folder.mkdir(parents=True, exist_ok=True)
        log_file = self.output_folder.resolve() / self.log_file_name
        logs.setup_logfile(log_file, level=logger.level)

        # copy over the input file
        shutil.copy(str(self.input_file.resolve()), str(self._input_filepath.resolve()))

        # copy additional files
        self._copy_additional_files()

        # save the parameters of the pipeline
        self._save_pipeline_parameters()

        # run the pipeline
        start = time.time()
        try:
            return self._run_pipeline()
        except Exception as e:
            logger.exception(f"Pipeline failed with {e}.")
            raise e
        finally:
            logger.info(f"Pipeline took {time.time()-start:.0f} seconds.")

            # de-register the logger file handler
            logs.remove_logfile(log_file)

            # remove the input file from the output folder
            self._input_filepath.unlink()

            # remove the output folder if needed
            if self.delete_output_folder:
                shutil.rmtree(str(self.output_folder.resolve()), ignore_errors=True)
                self.output_folder = None


    def _copy_additional_files(self):
        pass
    

    def _save_pipeline_parameters(self):
        raise NotImplementedError


    def _run_pipeline(self):
        # run each part of the pipeline, tracking where it fails
        failed_at = None
        for process_call, input, output, identifier in self._pipeline:
            if not self._run_step(process_call, input, output, identifier): 
                logger.info(f"Pipeline failed at step {identifier}.")
                failed_at = identifier
                break

        # check overall success criteria
        if failed_at:
            logger.info(f"Pipeline failed, due to failure at {failed_at}.")
            success = False
        else:
            custom_success = self._custom_success_criteria()
            success = output.exists() and custom_success
            logger.info(f"Pipeline result: {success}. Output exists: {output.exists()}, custom criteria: {custom_success}.")

        # save the pipeline results
        d = {
            'success': success,
            'failed_at': failed_at,
            'iteration': self.iteration,
            'input': self.input_file.name
        }
        d = self._customize_results(d)
        self.results.append(d)

        return self.results.to_df(), self.metadata.to_df()

    
    def _run_step(self, process_call, input: pathlib.Path, output: pathlib.Path, identifier: str):
        # run the process
        logger.debug(f"Running {identifier}")
        metadata = process_call(
            input, 
            output, 
            process_log_file = self.output_folder / (identifier + self.process_log_file_suffix),
            timeout = self.process_timeout
        )

        # we measure success by the return code and whether the output file exists
        success = (metadata['return_code'] == 0) and output.exists()
        if not success:
            logger.warning(f"Process {identifier} failed with return code {metadata['return_code']}, output exists: {output.exists()}.")

        # include additional data in the metadata
        metadata['identifier'] = identifier
        metadata['success'] = success
        metadata['iteration'] = self.iteration
        metadata['input'] = self.input_file.name
        
        # include custom data in the metadata
        metadata = self._customize_metadata(metadata)

        # save metadata
        self.metadata.append(metadata)

        # return success
        return metadata['success']
    

    def _custom_success_criteria(self):
        return True

    def _customize_results(self, results):
        return results

    def _customize_metadata(self, metadata):
        return metadata