import numpy as np

import db
from __init__ import logger
from material import Material


def reverse_search_attribute(target: int, vector: np.ndarray, dim: int):
    if dim < 2:
        msg = 'dim must be <= 2'
        logger.error(msg)
        raise ValueError(msg)

    matrix = vector
    for _ in range(dim):
        matrix = np.add.outer(matrix, vector)

    indices = np.argwhere(matrix == target).sort()
    indices = np.unique(indices, axis=0)  # Remove duplicates
    # Remove repeating materials, eg [1, 1, 4]
    # Todo: For every row
    filter = indices[:-1][indices[1:] == indices[:-1]]
    # Todo: if filter is not empty, remove


def reverse_search(name: str, ingredients: int = 3) -> [[Material]]:
    result, candidates = db.fetch_set_by_name(name)
    candidates = np.array(candidates)[:, 2:]  # Remove first to entries from every row
    candidates = candidates.astype(np.int8)  # Set to appropriate data type

    # From smallest to highest attribute value
    hits = []
    indices = np.array(result.attributes.values()).argsort()
    for i in indices:
        hits.append(reverse_search_attribute(candidates[:, i], result.attributes[i], dim=ingredients))
        # Todo: Filter out non hits to shrink down solution space


if __name__ == '__main__':
    db.create_table()
    logger.info(reverse_search('0'))
