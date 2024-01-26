"""
Compare
-------

Function for finding how many of an entity will fit inside a container.
"""

from howmany.utils import (
    _get_ent_label,
    _get_ent_prop_amount,
    _get_ent_prop_amount_unit,
)


def compare(
    containers: str | list = "Q183",
    entities: str | list = "Q8524",
    pid: str = "P2046",
    iso: str = "en",
):
    """
    Compare the size of passed entities and containers.

    Parameters
    ----------
        containers : str or list of strings (default=Q183)
            The numerators of the desired ratios.

        entities : str or list of strings (default=Q8524)
            The denominators of the desired ratios.

        pid : str (default=P2046)
            The property identifier for a comparison that should be made.

        iso : str (default=en)
            The ISO 2 code for a language for which the label should be returned for.

    Returns
    -------
        ratios_dict : dict
            A dictionary of entity and container labels and their ratios for the property.
    """
    containers = [containers] if isinstance(containers, str) else containers
    entities = [entities] if isinstance(entities, str) else entities

    try:
        container_units = [
            _get_ent_prop_amount_unit(qid=c, pid=pid) for c in containers
        ]

        container_amounts = [_get_ent_prop_amount(qid=c, pid=pid) for c in containers]
        entity_amounts = [
            _get_ent_prop_amount(qid=e, pid=pid, unit=container_units[i])
            for i, e in enumerate(entities)
        ]

    except KeyError:
        entity_units = [_get_ent_prop_amount_unit(qid=e, pid=pid) for e in entities]
        container_amounts = [
            _get_ent_prop_amount(qid=c, pid=pid, unit=entity_units[i])
            for i, c in enumerate(containers)
        ]
        entity_amounts = [_get_ent_prop_amount(qid=e, pid=pid) for e in entities]

    container_labels = [_get_ent_label(qid=c, iso=iso) for c in containers]
    entity_labels = [_get_ent_label(qid=e, iso=iso) for e in entities]

    ratios_dict = {}
    for c, c_lbl in enumerate(container_labels):
        for e, e_lbl in enumerate(entity_labels):
            ratios_dict[c_lbl] = {
                "entity": e_lbl,
                "amount": container_amounts[c] / entity_amounts[e],
            }

    return ratios_dict
