"""
In
--

Functions for finding how many of an object will fit inside another.
"""

from wikidata.client import Client

client = Client()
germany_entity = client.get("Q183", load=True).data
germany_label = germany_entity["labels"]["en"]["value"]
germany_area = float(germany_entity["claims"]["P2046"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])

soccer_field_entity = client.get("Q8524", load=True).data
soccer_field_entity_label = soccer_field_entity["labels"]["en"]["value"]
soccer_field_length = float(soccer_field_entity["claims"]["P2043"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
soccer_field_width = float(soccer_field_entity["claims"]["P2049"][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
soccer_field_area = soccer_field_length / 1000 * soccer_field_width / 1000

num_soccer_fields_per_germany = round(germany_area / soccer_field_area, 2)

print(f"You could fit {num_soccer_fields_per_germany:,} {soccer_field_entity_label}es inside {germany_label}.")
