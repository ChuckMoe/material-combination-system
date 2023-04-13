# Alchemical Point Buy System
## Intention
I wanted to create a system agnostic alchemical system for rpg's.
It should be reproducible, explainable and give players the option to
experiment on their own.

## Features
- Reproducible: Every time you combine the same materials, the result will be
the same. In theory.
- Explainable: Every material has a set of properties. Summing them up gives
you the result.
- Experiment: Don't tell your players the attributes of a material. Let them
research them or simply find new recipes by trial & error!

## Materials

Every material is unique, both in its name and in its combination of attributes.
Meaning no two materials will have the exact same attributes.
Every material can also have a description.

Example:
```
Dirt    | Absorbance: 5
Stone   | Absorbance: 1
Wood    | Absorbance: 5     - Not allowed   
```

### Attributes
All attributes are defined in the ```attributes.yml``` file. Changing this file
will affect **new** databases and materials.

#### Standard attributes
Below you will find a list of standard attributes used with this project. This
list may change in the future. It tries to represent the most basic attributes
of materials.

- hardness
- toughness
- stiffness
- ductility
- strength
- absorbance
- corrosion_resistance
- reactivity
- acidity
- electrical_capacitance
- magic_capacitance
- magic_affinity: Affinity to a certain kind of magic

#### Ranges
Depending on what kind of material you want to create, you should think about
your attribute ranges.

Are you looking for realism? Then how about a range from 0 to 99, putting
everything in relative relation.

Are you looking for a rarity approach? Then scale the attribute ranges by
rarity.

<table>
<thead>
  <tr>
    <th>Range</th>
    <th>Rarity</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0 - 10</td>
    <td>Common</td>
  </tr>
  <tr>
    <td>20 - 40</td>
    <td>Uncommon</td>
  </tr>
  <tr>
    <td>80 - 120</td>
    <td>Rare</td>
  </tr>
  <tr>
    <td>240 - 320</td>
    <td>Epic</td>
  </tr>
  <tr>
    <td>640 - 800</td>
    <td>Legendary</td>
  </tr>
</tbody>
</table>

### Combining Materials
If you want to combine or mix some materials to get another, more potent one,
simply add all attributes individually. The resulting material is the one with
the exact set of attributes.

Example:
```
Dirt    | Absorbance: 5, Ractivity: 4, Corrosion Resistance: 1
Stone   | Absorbance: 1, Strength: 7, Corrosion Resistance: 3
->
Some Material
Absorbance: 6, Ractivity: 4, Strength: 7, Corrosion Resistance: 4
```

## Rule Options
### Variations
To not always get the exact same material when combining, you can introduce
uncertainties. Let's say you already know a certain combination results in a
healing potion giving you 1d10 hp. What happens if you mix it in a hurry or in
an unclean environment though? You introduce a chance for variation because you
might miscalculate the exact amount or add bacteria by chance. So decide on how
big the chance is to introduce variation and roll (you or the player) a d100
to see if there is variation. Roll a d2 to see if its good / strengthening or
bad / debilitating

### Example Tables

<table>
<thead>
  <tr>
    <th>Dice</th>
    <th>Variation</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Head</td>
    <td>Good</td>
  </tr>
  <tr>
    <td>Tail</td>
    <td>Bad</td>
  </tr>
</tbody>
</table>

<table>
<thead>
  <tr>
    <th>Dice</th>
    <th>Variation</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0 - 5</td>
    <td>Extreme</td>
  </tr>
  <tr>
    <td>6 - 20</td>
    <td>High</td>
  </tr>
  <tr>
    <td>21 - 40</td>
    <td>Small</td>
  </tr>
  <tr>
    <td>41 - 99</td>
    <td>None</td>
  </tr>
</tbody>
</table>

## Todos
- Command line interface
- Reverse search: Specify an item and get examples on possible combinations
