import dataclasses
import pathlib
import math

from .abstractcodec import AbstractCodec
from ..tools import SubProcess

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclasses.dataclass
class DNAFountainCodec(AbstractCodec):
    """ 
    Implements the codec by XXX, based on XXX and available at XXX. 
    
    After initialization, the codec can be used to encode and decode files by calling encode() and decode().
    """

    # executable paths
    command_path_encode: str = dataclasses.field(default_factory = lambda: str(pathlib.Path(__file__).parent.absolute() / 'dnafountain' / 'encode.sh'))
    command_path_decode: str = dataclasses.field(default_factory = lambda: str(pathlib.Path(__file__).parent.absolute() / 'dnafountain' / 'decode.sh'))

    # codec settings
    size: int = 32              # size of the encoded chunks in bytes
    alpha: float = 0.07         # ratio of additional redundancy sequences to add
    file_size: int = 0          # size of file to encode in bytes

    # derived codec parameters
    chunk_size = property(lambda self: math.ceil((int(self.file_size)/int(self.size))))
    oligo_length = property(lambda self: int(self.size)*4+24)


    # 
    # encoding and decoding
    # 

    def _run_encoding(self, input_file: pathlib.Path, sequence_file: pathlib.Path, **kwargs):

        cmd = [self.command_path_encode]

        # add required arguments
        cmd.append(str(input_file.resolve()))
        cmd.append(str(sequence_file.resolve()))
        cmd.extend(['--size', str(self.size)])
        cmd.extend(['--alpha', str(self.alpha)])
        cmd.append('--no_fasta')

        return SubProcess(cmd, **kwargs)
        
    

    def _run_decoding(self, sequence_file: pathlib.Path, output_file: pathlib.Path, **kwargs):

        cmd = [self.command_path_decode]

        # add required arguments
        cmd.append(str(sequence_file.resolve()))
        cmd.append(str(output_file.resolve()))
        cmd.append(str(self.oligo_length))
        cmd.extend(['--chunk_num', str(self.chunk_size)])
        cmd.extend(['--size', str(self.size)])
        
        return SubProcess(cmd, **kwargs)
    
