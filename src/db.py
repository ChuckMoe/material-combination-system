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
    sql = "CREATE TABLE materials(name TEXT UNIQUE, description TEXT, {}, PRIMARY KEY({}))"
    sql = sql.format(attributes, ','.join(Material.attributes))
    logger.debug(sql)
    try:
        cursor.execute(sql)
    except sqlite3.DatabaseError:
        logger.warn('DB already exists. Not recreating.')


def fetch_all() -> [Material]:
    sql = 'SELECT * FROM materials'
    logger.debug(sql)

    materials = []
    for row in cursor.execute(sql):
        attributes = {key: row[i + 2] for i, key in
                      enumerate(Material.attributes)}
        materials.append(Material(row[0], row[1], **attributes))
    return materials


def __fetch_by(where: str, values: list):
    sql = f'SELECT * FROM materials WHERE {where}'
    logger.debug(sql)

    materials = []
    for row in cursor.execute(sql, values):
        attributes = {key: row[i + 2] for i, key in enumerate(Material.attributes)}
        materials.append(Material(row[0], row[1], **attributes))

    if materials:
        return materials
    else:
        logger.error(f'There is no material: {values}')
        return []


def fetch_by_name(name: str) -> Material:
    return __fetch_by('name = ?', [name])[0]


def fetch_by_attributes(attributes: [str], attribute_values: [[int]]) -> [Material]:
    template = '{} = ?'
    where = [template.format(key) for key in attributes]
    where = ' AND '.join(where)

    where = [f'({where})' for _ in range(len(attribute_values))]
    where = ' OR '.join(where)

    flatt_values = []
    for item in attribute_values:
        for attribute_value in item:
            flatt_values.append(attribute_value)

    return __fetch_by(where, flatt_values)


def fetch_set_by_name(name: str):
    result = fetch_by_name(name)

    where = ['{} <= ?'.format(key, value) for key, value in result.attributes.items()]
    sql = 'SELECT * FROM materials WHERE name != ? AND {}'.format(' AND '.join(where))
    logger.debug(sql)

    try:
        rows = cursor.execute(sql, [name, *result.attributes.values()]).fetchall()
        logger.debug(f'Possible Materials: {len(rows)}')
        return result, rows
    except sqlite3.DatabaseError as e:
        logger.error(e)


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
            f'Material with same attributes or name as {material.name} '
            f'already exists')


def insert(materials: [Material]):
    for material in materials:
        _insert(material)
    connection.commit()
