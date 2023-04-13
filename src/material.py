import random

import yaml


def load_attributes():
    with open('attributes.yml', 'r') as handler:
        attributes = yaml.load(handler, Loader=yaml.CLoader)
    return sorted(attributes)


def combine(*args) -> dict:
    """Separately sums up all attributes of the given materials"""
    attributes = {key: 0 for key in Material.attributes}
    for material in args:
        for key, value in material.attributes.items():
            attributes[key] += value
    return attributes


class Material:
    attributes = load_attributes()

    def __init__(self, name, description="", *args, **kwargs):
        self.name = name
        self.description = description
        self.attributes = {key: 0 for key in Material.attributes}

        for key, value in kwargs.items():
            if key in Material.attributes:
                self.attributes[key] = value

    def __str__(self):
        rep = self.name if self.description == '' else f'{self.name} - ' \
                                                       f'{self.description}'
        kv_list = []
        for key, value in self.attributes.items():
            if value > 0:
                kv_list.append(f'{key}: {value}')
        kv_list = ', '.join(kv_list)
        return f'{rep} | {kv_list}'

    def randomise_attributes(self, minimum: int = 0, maximum: int = 9):
        for key in self.attributes:
            self.attributes[key] = random.randint(minimum, maximum)
        return self
