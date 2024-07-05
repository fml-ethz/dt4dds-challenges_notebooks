import time
import pathlib
import dataclasses

from ..tools import logs, FileDataFrame

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



@dataclasses.dataclass
class Manager():
    """  """

    # main settings
    pipelines: list                      # list of pipelines to run
    save_log: bool = False               # whether to collect and save the logs
    save_dataframes: bool = False        # whether to save the dataframes during runtime
    output_folder: pathlib.Path = "."    # folder to save the results in

    # file-related settings
    log_file = 'pipeline.log'
    pipeline_results_file = 'pipeline_results.csv'
    performance_results_file = 'performance_results.csv'

    # properties
    _log_filepath = property(lambda self: self.output_folder.resolve() / self.log_file)
    _pipeline_results_filepath = property(lambda self: self.output_folder.resolve() / self.pipeline_results_file)
    _performance_results_filepath = property(lambda self: self.output_folder.resolve() / self.performance_results_file)


    def run(self):
        """  """
        start = time.time()
        logger.info(f"Running {len(self.pipelines)} pipelines.")

        # create the output folder
        if self.output_folder.exists():
            raise FileExistsError(f"Output folder {self.output_folder} already exists.")
        else:
            self.output_folder.mkdir(parents=True)

        # initialize the dataframes for the results
        self.pipeline_results = FileDataFrame(self._pipeline_results_filepath, save_on_append=self.save_dataframes)
        self.performance_results = FileDataFrame(self._performance_results_filepath, save_on_append=self.save_dataframes)

        # set up the log file, if needed
        if self.save_log:
            logs.setup_logfile(self._log_filepath, level=logger.level)

        # iterate over the pipelines
        for i, pipeline in enumerate(self.pipelines):
            logger.info(f"Running pipeline: {pipeline} ({i+1}/{len(self.pipelines)})")
            self._run_pipeline(pipeline)

        # save the dataframes, if needed
        if self.save_dataframes:
            self.pipeline_results.to_csv()
            self.performance_results.to_csv()

        # remove the connection to the log file, if needed
        if self.save_log:
            logs.remove_logfile(self._log_filepath)

        # finish up
        logger.info(f"Finished running pipelines in {time.time() - start:.0f} seconds.")
        return self.pipeline_results.to_df(), self.performance_results.to_df()


    def _run_pipeline(self, pipeline):
        # run the pipeline
        try:
            pipeline_results, performance_results = pipeline.run()
        except Exception as e:
            logger.exception(f"Pipeline {pipeline} failed with {e}.")
            raise e

        # add the results to the dataframes
        self.pipeline_results.extend(pipeline_results.to_dict(orient='records'))
        self.performance_results.extend(performance_results.to_dict(orient='records'))