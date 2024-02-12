"""
Compare
-------

A function for finding how many of an entity will fit inside another.
"""

from howmany.utils import (
    get_wd_ent_label,
    get_wd_ent_prop_amount,
    get_wd_ent_prop_amount_unit,
)


def compare(
    containers: str | list = None,
    container_amounts: int | list = None,
    container_units: str | list = None,
    entities: str | list = None,
    entity_amounts: int |list = None,
    entity_units: str | list = None,
    pid: str = None,
    iso: str = "en",
):
    """
    Compare the size of passed entities and containers.

    Parameters
    ----------
        containers : str or list of strings (default=None)
            The QIDs or labels of the numerators of the desired ratios.

        container_amounts : int or list of ints (default=None)
            Amounts for containers provided directly and not referenced from Wikidata.

        container_units : str or list of strings (default=None)
            Units for container amounts provided directly and not referenced from Wikidata.

        entities : str or list of strings (default=None)
            The QIDs or labels of the denominators of the desired ratios.

        entity_amounts : int or list of ints (default=None)
            Amounts for entities provided directly and not referenced from Wikidata.

        entity_units : str or list of strings (default=None)
            Units for entity amounts provided directly and not referenced from Wikidata.

        pid : str (default=None)
            The property identifier for a comparison that should be made.

        iso : str (default=en)
            The ISO 2 code for a language for which the label should be returned for.

    Returns
    -------
        ratios_dict : dict
            A dictionary of entity and container labels and their ratios for the property.
    """
    error_msg = (
        "There is a mismatch between the given units and what can be found on Wikidata."
    )

    containers = [containers] if isinstance(containers, str) else containers
    entities = [entities] if isinstance(entities, str) else entities

    if container_amounts is not None:
        assert container_units is not None, "Please provide units for the `container_amounts` argument."

        container_amounts = [container_amounts] if isinstance(container_amounts, int) else container_amounts
        container_units = [container_units] if isinstance(container_units, str) else container_units

        try:
            entity_amounts = [
                get_wd_ent_prop_amount(qid=e, pid=pid, unit=container_units[i])
                for i, e in enumerate(entities)
            ]

        except KeyError as e1:
            raise KeyError(error_msg) from e1

        container_labels = containers
        entity_labels = [get_wd_ent_label(qid=e, iso=iso) for e in entities]

    elif entity_amounts is not None:
        assert entity_units is not None, "Please provide units for the `entity_amounts` argument."

        entity_amounts = [entity_amounts] if isinstance(entity_amounts, int) else entity_amounts
        entity_units = [entity_units] if isinstance(entity_units, str) else entity_units

        try:
            container_amounts = [
                get_wd_ent_prop_amount(qid=c, pid=pid, unit=entity_units[i])
                for i, c in enumerate(containers)
            ]

        except KeyError as e2:
            raise KeyError(error_msg) from e2

        container_labels = [get_wd_ent_label(qid=c, iso=iso) for c in containers]
        entity_labels = entities

    else:
        try:
            container_units = [
                get_wd_ent_prop_amount_unit(qid=c, pid=pid) for c in containers
            ]

            container_amounts = [get_wd_ent_prop_amount(qid=c, pid=pid) for c in containers]
            entity_amounts = [
                get_wd_ent_prop_amount(qid=e, pid=pid, unit=container_units[i])
                for i, e in enumerate(entities)
            ]

        except KeyError:
            entity_units = [get_wd_ent_prop_amount_unit(qid=e, pid=pid) for e in entities]

            container_amounts = [
                get_wd_ent_prop_amount(qid=c, pid=pid, unit=entity_units[i])
                for i, c in enumerate(containers)
            ]
            entity_amounts = [get_wd_ent_prop_amount(qid=e, pid=pid) for e in entities]

        container_labels = [get_wd_ent_label(qid=c, iso=iso) for c in containers]
        entity_labels = [get_wd_ent_label(qid=e, iso=iso) for e in entities]

    ratios_dict = {}
    for c, c_lbl in enumerate(container_labels):
        for e, e_lbl in enumerate(entity_labels):
            ratios_dict[c_lbl] = {
                "entity": e_lbl,
                "amount": container_amounts[c] / entity_amounts[e],
            }

    return ratios_dict
