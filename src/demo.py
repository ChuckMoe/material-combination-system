import db
from combination import combine
from material import Material
from reverse_search import reverse_search

if __name__ == '__main__':
    db.create_table()
    materials = [
        Material(
            'Fire Herb',
            hardness=1,
            toughness=2,
            strength=5,
            acidity=3,
            magic_affinity=4),
        Material(
            'Ice Herb',
            hardness=1,
            toughness=2,
            strength=5,
            acidity=2,
            magic_affinity=4),
        Material(
            'Bark Herb',
            hardness=1,
            toughness=2,
            strength=5,
            acidity=1,
            magic_affinity=4),
        Material(
            'Water Herb',
            hardness=1,
            toughness=2,
            strength=5,
            acidity=0,
            magic_affinity=4),
        Material(
            'Fire Resistance Potion',
            hardness=3,
            toughness=6,
            strength=15,
            acidity=6,
            magic_affinity=12),
        Material(
            'Steam Potion',
            hardness=2,
            toughness=4,
            strength=10,
            acidity=5,
            magic_affinity=8)
    ]
    # materials = [Material(f'{i}', strength=i, absorbance=i) for i in
    # range(100)]
    # materials = [Material(f'{i}').randomise_attributes() for i in range(
    # 100000)]
    db.insert(materials)
    combinations = reverse_search('Fire Resistance Potion', ingredients=3)
    combine([materials[0], materials[1]])
