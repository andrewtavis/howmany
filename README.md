<div align="center">
  <a href="https://github.com/andrewtavis/howmany"><img src="https://raw.githubusercontent.com/andrewtavis/howmany/main/.github/resources/logo/howmany_logo_transparent.png" width=545 height=150></a>
</div>

<ol></ol>

[![pyversions](https://img.shields.io/pypi/pyversions/howmany.svg?logo=python&logoColor=FFD43B&color=306998)](https://pypi.org/project/howmany/)
[![pypi](https://img.shields.io/pypi/v/howmany.svg?color=4B8BBE)](https://pypi.org/project/howmany/)
[![pypistatus](https://img.shields.io/pypi/status/howmany.svg)](https://pypi.org/project/howmany/)
[![license](https://img.shields.io/github/license/andrewtavis/howmany.svg)](https://github.com/andrewtavis/howmany/blob/main/LICENSE.txt)
[![coc](https://img.shields.io/badge/coc-Contributor%20Covenant-ff69b4.svg)](https://github.com/andrewtavis/howmany/blob/main/.github/CODE_OF_CONDUCT.md)
[![codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Wikidata powered comparisons

**howmany** is a Python package that leverages the [Wikidata](https://www.wikidata.org/) [REST API](https://www.wikidata.org/wiki/Wikidata:REST_API) to easily find and compare the dimensions of any object. You can use howmany to find the answers to questions including:

- How tall is the [Eiffel Tower](https://www.wikidata.org/wiki/Q243)?
- How many [association football pitches](https://www.wikidata.org/wiki/Q8524) would fit inside [Germany](https://www.wikidata.org/wiki/Q183) (or that new giant wind farm)?
- And eventually anything else that [Wikidata](https://www.wikidata.org/) has dimensions for!

Of note is also that howmany can do unit conversions for users in comparison calculations.

<a id="contents"></a>

# **Contents**

- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Examples](#examples)
- [To-Do](#to-do)

<a id="installation"></a>

# Installation [`⇧`](#contents)

howmany can be downloaded from PyPI via pip or sourced directly from this repository:

```bash
pip install howmany
```

```bash
git clone https://github.com/andrewtavis/howmany.git
cd howmany
python setup.py install
```

```python
import howmany
```

<a id="environment-setup"></a>

# Environment Setup [`⇧`](#contents)

The development environment for howmany can be installed via the following steps:

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the [howmany repo](https://github.com/andrewtavis/howmany), clone your fork, and configure the remotes:

> [!NOTE]
>
> <details><summary>Consider using SSH</summary>
>
> <p>
>
> Alternatively to using HTTPS as in the instructions below, consider SSH to interact with GitHub from the terminal. SSH allows you to connect without a user-pass authentication flow.
>
> To run git commands with SSH, remember then to substitute the HTTPS URL, `https://github.com/...`, with the SSH one, `git@github.com:...`.
>
> - e.g. Cloning now becomes `git clone git@github.com:<your-username>/howmany.git`
>
> GitHub also has their documentation on how to [Generate a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) 🔑
>
> </p>
> </details>

```bash
# Clone your fork of the repo into the current directory.
git clone https://github.com/<your-username>/howmany.git
# Navigate to the newly cloned directory.
cd howmany
# Assign the original repo to a remote called "upstream".
git remote add upstream https://github.com/andrewtavis/howmany.git
```

- Now, if you run `git remote -v` you should see two remote repositories named:
  - `origin` (forked repository)
  - `upstream` (howmany repository)

2. Use [Anaconda](https://www.anaconda.com/) to create the local development environment within your howmany directory:

   ```bash
   conda env create -f environment.yml
   ```

<a id="examples"></a>

# Examples [`⇧`](#contents)

See the [example Jupyter notebook](https://github.com/andrewtavis/howmany/tree/main/examples/howmany_examples.ipynb) for full examples.

```py
import howmany
from howmany.utils import (
    float_to_str,
    get_wd_ent_label,
    get_wd_ent_prop_amount,
    get_wd_ent_prop_amount_unit,
)
```

### Getting labels, amounts and units

```py
eiffel_tower_qid = "Q243"
height_pid = "P2048"

eiffel_tower_label = get_wd_ent_label(qid=eiffel_tower_qid)
eiffel_tower_height = get_wd_ent_prop_amount(qid=eiffel_tower_qid, pid=height_pid)
eiffel_tower_height_unit = get_wd_ent_prop_amount_unit(qid=eiffel_tower_qid, pid=height_pid)

print(
    f"The {eiffel_tower_label} is {round(eiffel_tower_height)} {eiffel_tower_height_unit}s tall."
)
# The Eiffel Tower is 324 metres tall.
```

### Simple comparisons of Wikidata items

```py
germany_qid = "Q183"
soccer_field_qid = "Q8524"
area_pid = "P2046"

soccer_fields_in_germany_dict = howmany.compare(
    containers=germany_qid, entities=soccer_field_qid, pid=area_pid
)

for k in soccer_fields_in_germany_dict.keys():
    amount = round(soccer_fields_in_germany_dict[k]["amount"], 2)
    print(
        f"You could fit {amount:,} {soccer_fields_in_germany_dict[k]['entity']}es inside {k}."
    )

# You could fit 50,453,300.88 association football pitches inside Germany.

germanies_in_soccer_fields_dict = howmany.compare(
    containers=soccer_field_qid, entities=germany_qid, pid=area_pid
)

for k in germanies_in_soccer_fields_dict.keys():
    amount = float_to_str(f=germanies_in_soccer_fields_dict[k]["amount"])
    print(
        f"You could fit {amount} {germanies_in_soccer_fields_dict[k]['entity']}s inside an {k}."
    )

# You could fit 0.0000000198 Germanys inside an association football pitch.
```

### Comparisons of Wikidata items with predefined amounts

```py
# Variables defined above...
giant_new_wind_farm_label = "giant new wind farm"
area_of_giant_new_wind_farm = 50
unit_of_giant_new_wind_farm_area = "square kilometre"

soccer_fields_in_giant_new_wind_farm_dict = howmany.compare(
    containers=giant_new_wind_farm_label,
    container_amounts=area_of_giant_new_wind_farm,
    container_units=unit_of_giant_new_wind_farm_area,
    entities=soccer_field_qid,
    pid=area_pid,
)

for k in soccer_fields_in_giant_new_wind_farm_dict.keys():
    amount = round(soccer_fields_in_giant_new_wind_farm_dict[k]["amount"], 2)
    print(
        f"You could fit {amount:,} {soccer_fields_in_giant_new_wind_farm_dict[k]['entity']}es inside the {k}."
    )

# You could fit 7,054.67 association football pitches inside the giant new wind farm.
```

### Comparisons across lists of containers or entities

```py
all_german_state_qids = ["Q64", ...]
saarland_qid = "Q1201"

saarlands_in_german_states_dict = howmany.compare(
    containers=all_german_state_qids, entities=saarland_qid, pid="P2046"  # , iso="en"
)

# Code to order labels and area ratios...

ax = sns.barplot(
    x=german_states_desc_saarland_area, y=german_state_desc_areas_in_saarlands
)
ax.set_title("Area of German States in Saarlands", size=18)
ax.set(xlabel="German State", ylabel="Area (Saarlands)")
ax.bar_label(ax.containers[0])
ax.xaxis.label.set_size(14)
ax.yaxis.label.set_size(14)
plt.xticks(rotation=45)

plt.show()
```

<div align="center">
  <a href="https://raw.githubusercontent.com/andrewtavis/howmany/main/examples/output_images/bar_german_states_by_saarland_area.png"><img src="https://raw.githubusercontent.com/andrewtavis/howmany/main/examples/output_images/bar_german_states_by_saarland_area.png" width=618 height=335></a>
</div>

<a id="to-do"></a>

# To-Do [`⇧`](#contents)

Please see the [contribution guidelines](https://github.com/andrewtavis/howmany/blob/main/CONTRIBUTING.md) if you are interested in contributing to this project. Work that is in progress or could be implemented includes:

- Work to be done is a work in progress, but suggestions welcome!

# Powered By

<div align="center">
  <br>
  <a href="https://www.wikidata.org/"><img height="175" src="https://raw.githubusercontent.com/andrewtavis/howmany/main/.github/resources/images/wikidata_logo.png" alt="Wikidata"></a>
  <br>
</div>
