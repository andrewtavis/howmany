"""
Utils
-----

Utility functions for accessing Wikidata's data with howmany.

Contents
--------
    float_to_str,
    _wd_rest_api_get_request,
    _get_ent_label,
    _get_ent_prop_amount_unit,
    _get_ent_prop_amount
"""


import decimal
from functools import reduce

import requests

pid_dimension_resolve_dict = {"P2046": ["P2043", "P2049"]}

base_unit_ratio_dict = {"square kilometre": {"metre": 1000, "centimetre": 100000}}

inv_base_unit_ratio_dict = {}
for u, rs in base_unit_ratio_dict.items():
    for target_u, r in rs.items():
        if target_u not in inv_base_unit_ratio_dict:
            inv_base_unit_ratio_dict[target_u] = {}
        inv_base_unit_ratio_dict[target_u][u] = 1 / r

unit_ratio_dict = base_unit_ratio_dict | inv_base_unit_ratio_dict


def float_to_str(f: float, prec: int = 20):
    """
    Converts a float into a long decimal string with a given precision.

    Parameters
    ----------
        f : float
            The float to be converted to a long decimal string.

        prec : int (default=20)
            The precision of the resulting decimal string.

    Returns
    -------
        f_string : str
            The original float formatted as a long decimal string.
    """
    ctx = decimal.Context()
    ctx.prec = prec

    f_string = ctx.create_decimal(repr(f))

    return format(f_string, "f")


def _wd_rest_api_get_request(qid: str, term: str = None):
    """
    Executes a get request against the Wikidata REST API.

    Parameters
    ----------
        qid : str
            The Wikidata QID that data should be returned for.

        term : str (default=None)
            The type of data that should be returned.

    Returns
    -------
        The JSON request value for the given item id and term.
    """
    api_endpoint = "https://www.wikidata.org/w/rest.php/wikibase/v0"
    request_string = f"{api_endpoint}/entities/items/{qid}"
    if term:
        request_string += f"/{term}"

    request = requests.get(request_string, timeout=5)

    return request.json()


def _get_ent_label(qid: str, iso: str = "en"):
    """
    Find the English label for the given Wikidata entity data.

    Parameters
    ----------
        qid : str
            The Wikidata QID that data should be returned for.

        iso : str (default=en)
            The ISO 2 code for a language for which the label should be returned for.

    Returns
    -------
        The label for the given Wikidata QID data and language iso code.
    """
    try:
        return _wd_rest_api_get_request(qid=qid, term="labels")[iso]

    except KeyError as e:
        raise KeyError(
            f"The qid {qid} does't have a label with the iso key {iso}."
        ) from e


def _get_ent_prop_amount_unit(qid: str, pid: str):
    """
    Find the value unit for the given Wikidata entity data.

    Parameters
    ----------
        qid : str
            The Wikidata QID that data should be returned for.

        pid : str
            The property identifier for a comparison that should be made.

    Returns
    -------
        The unit for the given Wikidata QID data and property identifier.
    """
    return _get_ent_label(
        qid=_wd_rest_api_get_request(qid=qid, term="statements")[pid][0]["value"][
            "content"
        ]["unit"].split("http://www.wikidata.org/entity/")[1],
        iso="en",
    )


def _get_ent_prop_amount(qid: str, pid: str, unit: str = None):
    """
    Find the value amount for the given Wikidata entity data.

    Parameters
    ----------
        qid : str
            The Wikidata QID that data should be returned for.

        pid : str
            The property identifier for a comparison that should be made.

        unit : str
            The unit of the amount that the returned amount should be compared to.

    Returns
    -------
        The amount for the given Wikidata QID data and property identifier.
    """
    error_msg = (
        f"The PID '{pid}' does not exist on the QID '{qid}' and cannot be resolved."
    )

    if unit:
        try:
            value_unit = _get_ent_prop_amount_unit(qid=qid, pid=pid)
        except KeyError:
            try:
                value_unit = _get_ent_prop_amount_unit(
                    qid=qid, pid=pid_dimension_resolve_dict[pid][0]
                )

            except KeyError as e1:
                raise KeyError(
                    f"Wikidata doesn't have units for the needed properties of {qid}."
                ) from e1
        unit_ratio = unit_ratio_dict[unit][value_unit]

    else:
        unit_ratio = 1

    try:
        amount = float(
            _wd_rest_api_get_request(qid=qid, term="statements")[pid][0]["value"][
                "content"
            ]["amount"][1:]
        )
    except KeyError as e2:
        if pid not in pid_dimension_resolve_dict:
            raise KeyError(error_msg) from e2

        amounts = []
        for r_pid in pid_dimension_resolve_dict[pid]:
            try:
                amounts.append(
                    float(
                        _wd_rest_api_get_request(qid=qid, term="statements")[r_pid][0][
                            "value"
                        ]["content"]["amount"][1:]
                    )
                    / unit_ratio
                )

                amount = reduce(lambda x, y: x * y, amounts)

            except KeyError as e3:
                raise KeyError(error_msg) from e3

    return amount
