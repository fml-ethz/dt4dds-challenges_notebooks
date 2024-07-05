import argparse

import simulator
simulator.tools.logs.setup_console()

import default_encodings

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

WORKFLOWS = {
    'test': simulator.workflows.NoWorkflow('test'),
    'decay': simulator.workflows.DecayChallengeWorkflow('decay-challenge'),
    'photolithography': simulator.workflows.PhotolithographyChallengeWorkflow('photolithography-challenge'),
}

def rmtree(root):
    if not root.exists():
        return
    for p in root.iterdir():
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()
    root.rmdir()

# parse the arguments
args = argparse.ArgumentParser(description="Run the simulation for all encodings.")
args.add_argument("workflow", type=str, help="The workflow to test: 'test', 'decay', or 'photolithography'.", choices=WORKFLOWS.keys())
args.add_argument("encoding", type=str, help="The encoding type to test: 'DNARS' or 'DBGPS'.", choices=default_encodings.ENCODINGS.keys())
args.add_argument("coderate", type=str, help="The code rate to test.")
args.add_argument("-i", "--iterations", type=int, default=3, help="Number of iterations to run each test for.")
args.add_argument("-f", "--force", action='store_true', help="Force deletion of the output folder if it already exists.")
args = args.parse_args()

# check & process the arguments
workflow = WORKFLOWS[args.workflow]
n_iterations = args.iterations
try:
    encoding = default_encodings.ENCODINGS[args.encoding][args.coderate]
except KeyError:
    raise ValueError(f"Invalid code rate '{args.coderate}' for the encoding '{args.encoding}', only {', '.join(default_encodings.ENCODINGS[args.encoding].keys())} are available.")
logger.info(f"Running encoding: {args.encoding}, {encoding['name']}")

# set up the output folder
output_folder = default_encodings.BASE_DIR / args.encoding / args.workflow / encoding['name']
if output_folder.exists():
    if args.force:
        logger.warning(f"Deleting the existing output folder: {output_folder}")
        rmtree(output_folder)
    else:
        raise FileExistsError(f"Output folder {output_folder} already exists.")

# create the pipelines
pipelines = simulator.pipeline.Pipeline.factory(
    input_file = simulator.INPUT_FILE,
    codec = encoding['codec'],
    workflow = workflow,
    codec_folder = encoding['directory'],
    iterations = n_iterations,
    output_folder = output_folder,
    process_timeout = 60*60*24,  # 24 hours
)

# run the pipelines with the manager
manager = simulator.pipeline.Manager(
    pipelines = pipelines,
    save_log = True,
    save_dataframes = True,
    output_folder = output_folder,
)
manager.run()