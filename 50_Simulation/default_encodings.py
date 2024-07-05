import pathlib

import simulator

BASE_DIR = pathlib.Path('../data_simulated/').resolve()
ENCODINGS = {
    'DNAFOUNTAIN': {},
    'DNARS': {},
    'DBGPS': {},
}

# 
# DNA FOUNTAIN CODEC
# 
_SETTINGS = [
    {
        'name': 'coderate_decay_0-50',
        'size': 32,
        'alpha': 2.4,
    }, {
        'name': 'coderate_decay_0-40',
        'size': 32,
        'alpha': 3.2,
    }, {
        'name': 'coderate_decay_0-30',
        'size': 32,
        'alpha': 4.6,
    }, {
        'name': 'coderate_decay_0-20',
        'size': 32,
        'alpha': 7.5,
    }, {
        'name': 'coderate_photolithography_0-50',
        'size': 14,
        'alpha': 1.8,
    }, {
        'name': 'coderate_photolithography_0-40',
        'size': 14,
        'alpha': 2.5,
    }, {
        'name': 'coderate_photolithography_0-30',
        'size': 14,
        'alpha': 3.6,
    }, {
        'name': 'coderate_photolithography_0-20',
        'size': 14,
        'alpha': 5.9,
    }

]

for setting in _SETTINGS:
    codec_dir = BASE_DIR / 'DNAFOUNTAIN' / 'design_seqs' / setting['name']
    
    codec = simulator.codecs.DNAFountainCodec(
        setting['name'],
        file_size = simulator.INPUT_FILE.stat().st_size,
        size = setting['size'],
        alpha = setting['alpha'],
    )

    ENCODINGS['DNAFOUNTAIN'][setting['name'].replace('coderate_', '').replace('-', '.')] = {
        'name': setting['name'],
        'directory': codec_dir,
        'codec': codec,
        'settings': setting,
    }





# 
# DNA RS CODEC
# 
_SETTINGS = [
    {
        'name': 'coderate_0-80',
        'seq_length': 72,
        'red_factor': 6,
        'num_seq': 7200,
    }, {
        'name': 'coderate_0-70',
        'seq_length': 72,
        'red_factor': 6,
        'num_seq': 8200,
    }, {
        'name': 'coderate_0-60',
        'seq_length': 72,
        'red_factor': 6,
        'num_seq': 9500,
    }, {
        'name': 'coderate_0-50',
        'seq_length': 72,
        'red_factor': 6,
        'num_seq': 11500,
    }
]

for setting in _SETTINGS:
    codec_dir = BASE_DIR / 'DNARS' / 'design_seqs' / setting['name']
    
    codec = simulator.codecs.DNARSCodec(
        setting['name'],
        file_size = simulator.INPUT_FILE.stat().st_size,
        seq_length = setting['seq_length'],
        red_factor = setting['red_factor'],
        num_seq = setting['num_seq'],
    )

    ENCODINGS['DNARS'][setting['name'].replace('coderate_', '').replace('-', '.')] = {
        'name': setting['name'],
        'directory': codec_dir,
        'codec': codec,
        'settings': setting,
    }





# 
# DBGPS CODEC
# 
_SETTINGS = [
    {
        'name': 'coderate_1-40',
        'droplet_num': 1800,
        'chunk_size': 35,
    }, {
        'name': 'coderate_1-30',
        'droplet_num': 1930,
        'chunk_size': 35,
    }, {
        'name': 'coderate_1-20',
        'droplet_num': 2100,
        'chunk_size': 35,
    }, {
        'name': 'coderate_1-10',
        'droplet_num': 2300,
        'chunk_size': 35,
    }
]

for setting in _SETTINGS:
    codec_dir = BASE_DIR / 'DBGPS' / 'design_seqs' / setting['name']

    codec = simulator.codecs.DBGPSCodec(
        setting['name'],
        file_size = simulator.INPUT_FILE.stat().st_size,
        droplet_num = setting['droplet_num'],
        chunk_size= setting['chunk_size'],
    )

    ENCODINGS['DBGPS'][setting['name'].replace('coderate_', '').replace('-', '.')] = {
        'name': setting['name'],
        'directory': codec_dir,
        'codec': codec,
        'settings': setting,
    }