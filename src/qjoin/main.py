import dataclasses
from typing import Iterable, Any, Tuple, List, Union, Callable, Hashable, Optional

import qjoin

@dataclasses.dataclass
class QjoinJoin:
    """
    Definition of a join in qjoin. We find there the collection to join, the field on which we perform the join.
    """
    collection: Iterable[Any]
    key: Optional[Union[str, Callable[[Any], Hashable]]] = None


class Qjoin:

    def __init__(self, collection: Iterable[Any]):
        self._base_collection = collection
        self.join_definitions: List['QjoinJoin'] = []

    def __iter__(self):
        predicates = []
        for join_definition in self.join_definitions:
            is_key_used = join_definition.key is not None
            is_key_str = join_definition.key is not None and isinstance(join_definition.key, str)
            is_key_func = join_definition.key is not None and callable(join_definition.key)

            predicate = lambda elt_left, elt_right: False
            if is_key_used and is_key_str:
                predicate = lambda elt_left, elt_right: elt_left[join_definition.key] == elt_right[join_definition.key]
            elif is_key_used and is_key_func:
                predicate = lambda elt_left, elt_right: join_definition.key(elt_left) == join_definition.key(elt_right)

            predicates.append(predicate)

        for element in self._base_collection:
            result = [element]
            for join_definition_index, join_definition in enumerate(self.join_definitions):
                join_match = False
                for element_to_join in join_definition.collection:
                    predicate = predicates[join_definition_index]
                    if predicate(element, element_to_join):
                        result.append(element_to_join)
                        join_match = True
                        break
                if join_match is False:
                    result.append(None)

            yield tuple(result)

    def join(self, collection: Iterable[Any], key: Union[str, Callable[[Any], Hashable]] = None) -> 'Qjoin':
        """
        Performs a join in a qjoin query with the base collection.

        ``join`` must define a join key. It is possible to use a simple key shared by the base collection
        and the collection to be joined with ``key`` parameter or to use a key specific to each collection
        with ``left`` and ``right`` parameters.

        A key can either be the name of a field in the collection, or a function that takes an element of
        the collection as a parameter and returns a value on which to join.

        A first technique is to use a simple key as the join key.

        >>> spacecrafts = [
        >>>    {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        >>>    {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        >>>    {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        >>>    {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        >>>    {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
        >>> ]
        >>>
        >>> global_spacecrafts = qjoin.on(spacecrafts).join(spacecrafts_properties, key='name')
        >>> for spacecraft, spacecraft_properties in global_spacecrafts:
        >>>     print(spacecraft['name'])
        >>>     print('-' * len(spacecraft['name']))
        >>>     print(spacecrafts_property['dimension'])
        >>>     print('')
        >>>     print('')

        A second technique is to use a function to generate a more complex join key.
        This function must return a hashable type in order to be used as a join key.

        >>> spacecrafts = [
        >>>    {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        >>>    {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        >>>    {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        >>>    {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        >>>    {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
        >>> ]
        >>>
        >>> global_spacecrafts = qjoin.on(spacecrafts).join(spacecrafts_properties, key=lambda s: s['name'].lower())
        >>> for spacecraft, spacecraft_properties in global_spacecrafts:
        >>>     print(spacecraft['name'])
        >>>     print('-' * len(spacecraft['name']))
        >>>     print(spacecrafts_property['dimension'])
        >>>     print('')
        >>>     print('')

        The join function is lazy. Until a render function is called like .all or a loop is used on the QJoin instance,
        the join is just declared.
        """
        if key is None:
            raise ValueError('A key has to be specified when using join in qjoin query. qjoin.join(key="mykey") or qjoin.join(key=lambda x: x.mykey)')

        join = QjoinJoin(collection, key)
        self.join_definitions.append(join)
        return self

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
    >>>
    >>> for spacecraft in qjoin.on(spacecrafts):
    >>>     print(spacecraft['name'])
    """
    return Qjoin(collection)
