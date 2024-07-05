import pathlib
import dataclasses
import yaml

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclasses.dataclass
class Step():
    """ Abstract class to implement common functionality for all processing steps. To be subclassed by abstract implementations of processing steps. """

    slug: str
    type = property(lambda self: self.__class__.__name__)
    identifier = property(lambda self: f"{self.type}-{self.slug}")
    parameters = property(lambda self: dataclasses.asdict(self))

    def __repr__(self):
        return self.identifier
    
    def __str__(self):
        return self.identifier

    def save_parameters(self, output_file: pathlib.Path):
        """ Save the parameters of the clustering algorithm to the output file. """
        logger.debug(f"Saving parameters of {self} to {output_file}.")
        with open(output_file, 'w') as f:
            yaml.dump(self.parameters, f, default_flow_style=False, sort_keys=False)