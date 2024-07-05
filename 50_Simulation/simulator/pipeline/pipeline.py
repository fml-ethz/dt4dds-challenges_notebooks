import pathlib
import dataclasses
import copy
import shutil

from .abstract_pipeline import AbstractPipeline
from ..codecs import AbstractCodec
from ..workflows import AbstractWorkflow
from ..tools import encoding_stats, compare_files

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



@dataclasses.dataclass
class Pipeline(AbstractPipeline):
    """  """

    # processing-related settings
    codec: AbstractCodec = None                 # codec to use
    workflow: AbstractWorkflow = None           # workflow to use

    # file-related settings
    codec_folder: pathlib.Path = None           # path to the folder with the codec output
    codec_output_file: str = 'design_seqs.txt'  # name of the file with the encoder output
    sequence_file: str = 'design_seqs.txt'      # name of the file with design sequences
    read_file: str = 'R1.fq.gz'                 # name of the sequencing file with the workflow output
    output_suffix: str = '.decoded'             # suffix for the recovered file to add to the name of the input file

    # filepaths for the parameters of each step
    codec_settings: str = 'params_codec.yaml'               # name of the file to save codec settings in
    workflow_settings: str = 'params_workflow.yaml'         # name of the file to save workflow settings in
    clustering_settings: str = 'params_clustering.yaml'     # name of the file to save clustering settings in

    # properties
    _sequence_filepath = property(lambda self: self.output_folder.resolve() / self.sequence_file)
    _read_filepath = property(lambda self: self.output_folder.resolve() / self.read_file)
    _output_filepath = property(lambda self: self.output_folder.resolve() / (self.input_file.name + self.output_suffix))

    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.input_file.name}, {self.codec.identifier}, {self.workflow.identifier})"


    @classmethod
    def factory(cls, 
        input_file: pathlib.Path,               # path to input file
        codec,                                  # codec to use
        workflow,                               # workflow to use
        codec_folder: pathlib.Path,             # path to the folder with the codec output
        iterations: int = None,                 # number of iterations to run each pipeline for
        output_folder: pathlib.Path = None,     # path to the output folder
        **kwargs
    ):
        """  """
        input_file = pathlib.Path(input_file)
        codec_folder = pathlib.Path(codec_folder)
        pipelines = []
        for i_iter in range(1, iterations+1) if iterations else [None]:
            # set up the output folder
            if output_folder:
                folder = pathlib.Path(output_folder)
                if i_iter: folder = folder / str(i_iter).zfill(2)
            else:
                folder = None

            # copy the kwargs for this pipeline
            ikwargs = copy.deepcopy(kwargs)

            # create the pipeline
            ikwargs.update(
                # processing-related settings
                input_file = input_file,
                codec = codec,
                workflow = workflow,
                codec_folder = codec_folder,
                iteration = i_iter,
                # file-related settings
                output_folder = folder,
            )
            pipelines.append(cls(**ikwargs))

        # return the pipeline instances
        logger.info(f"Generated {len(pipelines)} pipelines.")
        return pipelines


    @property
    def _pipeline(self):
        return [
            (self.workflow.run, self._sequence_filepath, self._read_filepath.parent, 'workflow'),
            (self.codec.decode, self._read_filepath, self._output_filepath, 'decoding'),
        ]


    def _copy_additional_files(self):
        # copy the codec output file with the design sequences
        shutil.copy(str(self.codec_folder.resolve() / self.codec_output_file), str(self._sequence_filepath.resolve()))


    def _save_pipeline_parameters(self):
        self.codec.save_parameters(self.output_folder.resolve() / self.codec_settings)
        self.workflow.save_parameters(self.output_folder.resolve() / self.workflow_settings)


    def _custom_success_criteria(self):
        return self._output_filepath.exists() and compare_files(str(self.input_file), str(self._output_filepath))


    def _customize_results(self, results):
        results['codec_type'] = self.codec.type
        results['codec_slug'] = self.codec.slug
        results['workflow_type'] = self.workflow.type
        results['workflow_slug'] = self.workflow.slug

        # add the encoding stats
        try:
            results.update(encoding_stats(self.input_file, self._sequence_filepath))
        except FileNotFoundError as e:
            logger.warning(f"Could not calculate encoding stats: {e}")
        return results


    def _customize_metadata(self, metadata):
        metadata['codec_type'] = self.codec.type
        metadata['codec_slug'] = self.codec.slug
        metadata['workflow_type'] = self.workflow.type
        metadata['workflow_slug'] = self.workflow.slug
        return metadata
