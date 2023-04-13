import db
from __init__ import logger
from material import combine, Material


if __name__ == '__main__':
    db.create_table()
    materials = db.fetch_all()
    materials.append(Material('dirt', description='dirty', absorbance=7))
    materials.append(Material('stone', absorbance=1))
    materials.append(Material('stone').randomise_attributes())  # Fails
    material = db.fetch_by_attributes(combine(materials[0], materials[1]))
    logger.info(material)

    db.insert(materials)
