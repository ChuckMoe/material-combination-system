import numpy as np

import db
from __init__ import logger
from material import Material


def remove_duplicate_materials_rows(dim, matrix) -> np.ndarray:
    logging_rows = matrix.shape[0]
    diff = np.diff(matrix)
    diff = np.argwhere(diff == 0)[:, 0].flatten()
    matrix = np.ma.array(matrix, mask=False)
    matrix.mask[diff] = True
    matrix = matrix.compressed().reshape((-1, dim))
    logger.debug(f'Removed {logging_rows - matrix.shape[0]} rows with repeating materials')
    return matrix.astype(dtype=np.uint8)


def remove_duplicate_rows(matrix) -> np.ndarray:
    logging_rows = matrix.shape[0]
    matrix = np.sort(matrix, axis=1)
    matrix = np.unique(matrix, axis=0)
    logger.debug(f'Removed {logging_rows - matrix.shape[0]} duplicate rows')
    return matrix


def calculate_matrix_addition(dim, vector) -> np.ndarray:
    matrix = vector
    for _ in range(dim - 1):
        matrix = np.add.outer(matrix, vector)
    return matrix


def reverse_search_attribute(vector: np.ndarray, target: int, dim: int):
    if dim < 2:
        msg = 'dim must be <= 2'
        logger.error(msg)
        raise ValueError(msg)

    dim_warn = 5
    if dim > dim_warn:
        logger.warn(f'Calculations with more than {dim_warn} is discouraged. This can take a while...')

    matrix = calculate_matrix_addition(dim, vector)
    indices = np.argwhere(matrix == target)
    indices = remove_duplicate_rows(indices)
    indices = remove_duplicate_materials_rows(dim, indices)
    return indices


def calculate_combinations_for_every_attribute(matrix: np.ndarray, dim: int, result: Material) -> np.ndarray:
    """
    :param matrix: Matrix of attributes smaller than the ones of result.
    :param dim: Dimension of solution space. Denotes the amount of ingredients.
    :param result: The resulting material you are searching for.
    :return: Matrix of combinations, resulting in result.
    """
    # From smallest to highest attribute value
    hits = []
    indices = np.array(list(result.attributes.values())).argsort()
    for i in indices:
        logger.info(f'Reverse search: {Material.attributes[i]} - {matrix.shape[0]} possibilites')
        r = reverse_search_attribute(matrix[:, i], result.attributes[Material.attributes[i]], dim=dim)
        solution_space = np.unique(r, axis=None)
        matrix = matrix[solution_space]
        hits.append(r)
    hits = np.concatenate(hits, dtype=np.uint8)
    return hits


def calculate_combinations_for_all_attributes(matrix: np.ndarray, result: Material) -> np.ndarray:
    """
    :param numpy.ndarray matrix: Matrix of material combinations
    :param result: The resulting material you are searching for.
    :return: Matrix of combinations for the material in question.
    """
    _, counts = np.unique(matrix, return_counts=True, axis=0)
    indices = np.argwhere(counts == len(result.attributes)).flatten()
    matrix = matrix[indices]
    matrix = remove_duplicate_rows(matrix)
    return matrix


def fetch_material_pool(candidates, hits, result) -> {tuple: Material}:
    """
    :return: Dict of unique material objects that are used in combinations.
    """
    material_indices = np.unique(hits)
    material_pool = candidates[material_indices]
    material_pool = db.fetch_by_attributes(result.attributes.keys(), material_pool.tolist())

    material_pool = {tuple(material.attributes.values()): material for material in material_pool}
    return material_pool


def reverse_search(name: str, ingredients: int = 3) -> [[Material]]:
    """
    :param name: Name of the material to search combinations for.
    :param ingredients: Number of ingredients to combine.
    :return: List of material lists that result in the material in question.
    """
    result, candidates = db.fetch_set_by_name(name)

    if result is None:
        raise NameError('No material with this name')

    if not candidates:
        return np.array([])

    candidates = np.array(candidates)[:, 2:]  # Remove first to entries from every row
    candidates = candidates.astype(np.uint8)

    hits = calculate_combinations_for_every_attribute(candidates, ingredients, result)
    hits = calculate_combinations_for_all_attributes(hits, result)
    logger.debug(f'Found {hits.shape[0]} combination(s)')
    if hits.shape[0] == 0:
        return []

    material_pool = fetch_material_pool(candidates, hits, result)

    combinations = []
    for row in hits.tolist():
        combinations.append([material_pool[tuple(candidates[element])] for element in row])

    return combinations


if __name__ == '__main__':
    db.create_table()
    # materials = [Material(f'{i}', strength=i, absorbance=i) for i in range(100)]
    # materials = [Material(f'{i}').randomise_attributes() for i in range(100000)]
    # db.insert(materials)
    logger.info(reverse_search('5', ingredients=3))
