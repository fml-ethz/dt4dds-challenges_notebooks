import dataclasses
import pathlib
import math

from .abstractcodec import AbstractCodec
from ..tools import SubProcess

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclasses.dataclass
class DBGPSCodec(AbstractCodec):
    """ 
    Implements the codec by XXX, based on XXX and available at XXX. 
    
    After initialization, the codec can be used to encode and decode files by calling encode() and decode().
    """

    # executable paths
    command_path_encode: str = dataclasses.field(default_factory = lambda: str(pathlib.Path(__file__).parent.absolute() / 'DBGPS' / 'encode.sh'))
    command_path_decode: str = dataclasses.field(default_factory = lambda: str(pathlib.Path(__file__).parent.absolute() / 'DBGPS' / 'decode.sh'))

    # codec settings
    droplet_num: int = 2000             # number of droplets
    chunk_size: int = 35                # size of the encoded chunks in bytes
    file_size: int = 0                  # size of file to encode in bytes

    # derived codec parameters
    chunk_num = property(lambda self: math.ceil(self.file_size/self.chunk_size))   # number of data chunks (chunk size=35), needed for decoding


    # 
    # encoding and decoding
    # 

    def _run_encoding(self, input_file: pathlib.Path, sequence_file: pathlib.Path, **kwargs):

        cmd = [self.command_path_encode]

        # add required arguments
        cmd.append(str(input_file.resolve()))
        cmd.append(str(sequence_file.resolve()))
        cmd.extend(['--droplet_num', str(self.droplet_num)])
        cmd.extend(['--chunk_size', str(self.chunk_size)])

        return SubProcess(cmd, **kwargs)
        
    
    def _run_decoding(self, sequence_file: pathlib.Path, output_file: pathlib.Path, **kwargs):

        cmd = [self.command_path_decode]

        # add required arguments
        cmd.append(str(sequence_file.resolve()))
        cmd.append(str(output_file.resolve()))
        cmd.extend(['--chunk_num', str(self.chunk_num)])
        cmd.extend(['--chunk_size', str(self.chunk_size)])
        
        return SubProcess(cmd, **kwargs)
    
