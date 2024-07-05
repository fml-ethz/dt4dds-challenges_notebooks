import pathlib

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def compare_files(original_file: pathlib.Path, compare_file: pathlib.Path) -> bool:
    """ Check if two files are equal by bytewise comparison. Ignores if the file to compare is longer than the original file."""
    with open(original_file, "rb") as f, open(compare_file, "rb") as g:
        i = 0
        while (byte := f.read(1)):
            i += 1
            try:
                other_byte = g.read(1)
                if byte != other_byte:
                    logger.info(f"Files are different at byte {i}: {byte} vs. {other_byte}")
                    return False
            except:
                return False
    return True