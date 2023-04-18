import db
from __init__ import logger
from material import Material


def combine(materials: [Material]) -> Material:
    """Separately sums up all attributes of the given materials"""
    if 2 > len(materials):
        raise ValueError('At least two materials must me specified')
    logger.info(' + '.join([m.name for m in materials]))

    attributes = {key: 0 for key in materials[0].attributes}
    for material in materials:
        for key, value in material.attributes.items():
            attributes[key] += value
    result = db.fetch_by_attributes(attributes.keys(), [attributes.values()])
    logger.info(f'\t{result[0]}')
    return result


class Combination:
    def __init__(self, result: Material, components: [Material]):
        self.result = result
        self.components = components

    def __str__(self) -> str:
        components = [c.name for c in self.components]
        # return '{}: {}'.format(self.result.name, ' + '.join(components))
        return '{}'.format(' + '.join(components))
