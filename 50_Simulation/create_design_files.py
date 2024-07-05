import yaml
import logging
logger = logging.getLogger(__name__)

import simulator
simulator.tools.logs.setup_console()

import default_encodings

def rmtree(root):
    if not root.exists():
        return
    for p in root.iterdir():
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()
    root.rmdir()



# go through all default encodings and encode the input file
for encoding_type, encodings in default_encodings.ENCODINGS.items():
    for encoding_name, encoding in encodings.items():

        # delete and re-create the codec directory
        codec_dir = encoding['directory']
        rmtree(codec_dir)
        codec_dir.mkdir(parents=True, exist_ok=True)

        # warn about DBGPS codec
        if encoding_type == "DBGPS":
            logger.warning("Code rates for DBGPS are not accurate. The codec requires specific primer adapters that are part of the design sequences, but should not be considered for the code rate.")

        # encode the input file
        codec = encoding['codec']
        codec.encode(simulator.INPUT_FILE, codec_dir / 'design_seqs.txt', process_log_file=codec_dir / 'encoding.log')
        
        # save encoding stats and settings
        stats = simulator.tools.stats.encoding_stats(simulator.INPUT_FILE, codec_dir / 'design_seqs.txt')
        stats['codec'] = codec.type
        stats.update(encoding['settings'])
        stats.update(codec.parameters)
        with open(codec_dir / 'encoding_stats.yaml', 'w') as f:
            yaml.dump(stats, f)