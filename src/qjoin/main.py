from typing import Iterable, Any, Tuple, List

import qjoin


class Qjoin:

    def __init__(self, collection: Iterable[Any]):
        self._base_collection = collection

    def __iter__(self):
        for element in self._base_collection:
            yield (element, )

    def all(self) -> List[Tuple[Any, ...]]:
        """
        Return the result of qjoin query in a list of tuple where the first element of base collection
        is the first element of the first tuple, the first element of the first join is the second in the tuple

        >>> spacecrafts = [
        >>>    {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        >>>    {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        >>>    {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        >>>    {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        >>>    {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
        >>> ]
        >>>
        >>> for spacecraft in qjoin.on(spacecrafts).all():
        >>>     print(spacecraft['name'])
        """
        return list(self)


def on(collection: Iterable[Any]) -> 'Qjoin':
    """
    Start a qjoin query on a collection

    >>> spacecrafts = [
    >>>    {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
    >>>    {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
    >>>    {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
    >>>    {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
    >>>    {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    >>> ]
    >>> for spacecraft in qjoin.on(spacecrafts):
    >>>     print(spacecraft['name'])
    """
    return Qjoin(collection)
