import sqlite3

from __init__ import logger
from material import Material

connection = sqlite3.connect("materials.db")
cursor = connection.cursor()


def create_table():
    template = '{} INTEGER'
    attributes = []

    for attribute in Material.attributes:
        attributes.append(template.format(attribute))
    attributes = ', '.join(attributes)
    sql = f"CREATE TABLE materials(name TEXT UNIQUE, description TEXT, " \
          f"{attributes}, PRIMARY KEY({','.join(Material.attributes)}))"
    try:
        cursor.execute(sql)
    except sqlite3.DatabaseError:
        logger.warn('DB already exists. Not recreating.')


def fetch_all() -> [Material]:
    sql = 'SELECT * FROM materials'
    materials = []
    for row in cursor.execute(sql):
        attributes = {key: row[i + 2] for i, key in
            enumerate(Material.attributes)}
        materials.append(Material(row[0], row[1], **attributes))
    return materials


def __fetch_by(where: str, value):
    sql = f'SELECT * FROM materials WHERE {where}'
    row = cursor.execute(sql, value).fetchone()
    if row is None:
        logger.error(f'There is no material: {value}')
        return None
    attributes = {key: row[i + 2] for i, key in enumerate(Material.attributes)}
    return Material(row[0], row[1], **attributes)


def fetch_by_name(name: str) -> [Material]:
    return __fetch_by('name = ?', name)


def fetch_by_attributes(attributes: dict[str, int]) -> [Material]:
    template = '{} = ?'
    where = [template.format(key) for key in attributes]
    where = ' AND '.join(where)
    return __fetch_by(where, list(attributes.values()))


def _insert(material: Material):
    keys = 'name,description,{}'.format(','.join(Material.attributes))
    values = [material.name, material.description,
        *material.attributes.values()]

    prepared = ','.join(['?'] * len(values))
    sql = f"INSERT INTO materials({keys}) VALUES ({prepared})"
    try:
        cursor.execute(sql, values)
    except sqlite3.DatabaseError:
        logger.warn(
            f'Material with same attributes as {material.name} already exists')


def insert(materials: [Material]):
    for material in materials:
        _insert(material)
    connection.commit()
