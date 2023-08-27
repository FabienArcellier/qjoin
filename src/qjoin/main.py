import dataclasses
from typing import Iterable, Any, Tuple, List, Union, Callable, Hashable, Optional, Type, TypeVar

import qjoin
from qjoin import logger

T = TypeVar('T')


@dataclasses.dataclass
class QjoinJoin:
    """
    Definition of a join in qjoin. We find there the collection to join, the field on which we perform the join.
    """
    collection: Iterable[Any]
    key: Optional[Union[int, str, Callable[[Any], Hashable]]] = None
    left: Optional[Union[int, str, Callable[[Any], Hashable]]] = None
    right: Optional[Union[int, str, Callable[[Any], Hashable]]] = None


class Qjoin:

    def __init__(self, collection: Iterable[Any]):
        self._base_collection = collection
        self.join_definitions: List['QjoinJoin'] = []

    def __iter__(self):
        predicates = []
        if _is_collection_empty(self._base_collection):
            return []

        for join_definition in self.join_definitions:
            is_key_used = join_definition.key is not None
            is_key_subscription = join_definition.key is not None and (isinstance(join_definition.key, str) or isinstance(join_definition.key, int))
            is_key_func = join_definition.key is not None and callable(join_definition.key)
            is_left_right_used = join_definition.key is None and join_definition.left is not None and join_definition.right is not None
            is_left_subscription = join_definition.left is not None and (isinstance(join_definition.left, str) or isinstance(join_definition.left, int))
            is_left_func = join_definition.left is not None and callable(join_definition.left)
            is_right_subscription = join_definition.right is not None and (isinstance(join_definition.right, str) or isinstance(join_definition.right, int))
            is_right_func = join_definition.right is not None and callable(join_definition.right)

            if _is_collection_subscriptable(self._base_collection):
                get_elt_left = lambda elt, key: elt[key]
            else:
                get_elt_left = lambda elt, key: getattr(elt, key)

            if _is_collection_empty(join_definition.collection):
                get_elt_right = lambda elt, key: None
            elif _is_collection_subscriptable(join_definition.collection):
                get_elt_right = lambda elt, key: elt[key]
            else:
                get_elt_right = lambda elt, key: getattr(elt, key)

            predicate = lambda elt_left, elt_right: False
            if is_key_used and is_key_subscription:
                predicate = lambda elt_left, elt_right: get_elt_left(elt_left, join_definition.key) == get_elt_right(elt_right, join_definition.key)
            elif is_key_used and is_key_func:
                predicate = lambda elt_left, elt_right: join_definition.key(elt_left) == join_definition.key(elt_right)
            elif is_left_right_used and is_left_subscription is True and is_right_subscription is True:
                predicate = lambda elt_left, elt_right: get_elt_left(elt_left, join_definition.left) == get_elt_right(elt_right, join_definition.right)
            elif is_left_right_used and is_left_func is True and is_right_subscription is True:
                predicate = lambda elt_left, elt_right: join_definition.left(elt_left) == get_elt_right(elt_right, join_definition.right)
            elif is_left_right_used and is_left_subscription is True and is_right_func is True:
                predicate = lambda elt_left, elt_right: get_elt_left(elt_left, join_definition.left) == join_definition.right(elt_right)
            elif is_left_right_used and is_left_func is True and is_right_func is True:
                predicate = lambda elt_left, elt_right: join_definition.left(elt_left) == join_definition.right(elt_right)

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

    def join(self, collection: Iterable[Any],
             key: Optional[Union[int, str, Callable[[Any], Hashable]]] = None,
             left: Optional[Union[int, str, Callable[[Any], Hashable]]] = None,
             right: Optional[Union[int, str, Callable[[Any], Hashable]]] = None) -> 'Qjoin':
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
        >>> spacecraft_properties = [
        >>>     {'name': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
        >>>     {'name': 'GRAIL (A)', 'launch_mass': 202.4},
        >>>     {'name': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        >>>     {'name': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
        >>> ]
        >>>
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

        >>>
        >>> global_spacecrafts = qjoin.on(spacecrafts).join(spacecrafts_properties, key=lambda s: s['name'].lower())
        >>> for spacecraft, spacecraft_properties in global_spacecrafts:
        >>>     print(spacecraft['name'])
        >>>     print('-' * len(spacecraft['name']))
        >>>     print(spacecrafts_property['dimension'])
        >>>     print('')
        >>>     print('')

        A third technique is to use a different key for each collection. This is useful when the key is different. The join
        has to be describe with left and right parameters. Parameters may be either a string or a function.

        >>> spacecraft_properties = [
        >>>     {'spacecraft': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
        >>>     {'spacecraft': 'GRAIL (A)', 'launch_mass': 202.4},
        >>>     {'spacecraft': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        >>>     {'spacecraft': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
        >>> ]
        >>> global_spacecrafts = qjoin.on(spacecrafts).join(spacecrafts_properties, left=lambda s: s['name'].lower(), right='spacecraft')

        The join function is lazy. Until a render function is called like .all or a loop is used on the QJoin instance,
        the join is just declared.
        """
        if key is None and left is None and right is None:
            raise ValueError('A key has to be specified when using join in qjoin query. qjoin.join(key="mykey") or qjoin.join(key=lambda x: x.mykey)')

        if key is not None and (left is not None or right is not None):
            raise ValueError('key parameter should be used alone, it must not be used with left or right parameters.')

        if left is not None and right is None:
            raise ValueError('A right key parameter has to be specified when using join in qjoin query and left. qjoin.join(left="any", right="mykey") or qjoin.join(left=lambda x: x.mykey, right=lambda x: x.mykey2)')

        join = QjoinJoin(collection, key=key, left=left, right=right)
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

    def as_aggregate(self, klass: Type[T], attributes: List[str]) -> List[T]:
        """
        Creates a list of type T objects from the data that has been joined. Data is written to the attributes specified
        in the attributes list in their join order.


        >>> @dataclasses.dataclass
        >>> class SpacecraftsAggregate:
        >>>   spacecraft: str
        >>>   properties: str

        >>> spacecrafts = [
        >>>   {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        >>>   {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        >>>   {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        >>>   {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        >>>   {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
        >>> ]

        >>> spacecraft_properties = [
        >>>   {'spacecraft': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
        >>>   {'spacecraft': 'GRAIL (A)', 'launch_mass': 202.4},
        >>>   {'spacecraft': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        >>>   {'spacecraft': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
        >>> ]
        >>>
        >>> for spacecraft in qjoin.on(spacecrafts) \
        >>>                        .join(spacecraft_properties, left='name', right='spacecraft') \
        >>>                        .as_aggregate(SpacecraftsAggregate, ['spacecraft', 'properties']]):
        >>>     print(spacecraft.properties['dimension'])
        """
        aggregates = []
        for elt in self:
            _instance = klass()
            for index, attr in enumerate(attributes):
                if not hasattr(_instance, attr):
                    logger.warning(f'Attribute {attr} is not defined in {klass.__name__} class.')

                setattr(_instance, attr, elt[index])

            if hasattr(_instance, '__post_qjoin__'):
                _instance.__post_qjoin__()

            aggregates.append(_instance)

        return aggregates


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


def _is_collection_subscriptable(collection: Iterable[Any]) -> bool:
    """
    Identifie si les éléments d'une collection sont adressés par index, comme par exemple pour une liste, un tuple ou un dictionnaire
    ou si les éléments sont adressés par clé, comme par exemple pour un dictionnaire ou par attribut, comme par exemple pour un objet.
    """
    first = next(collection.__iter__())
    return hasattr(first, '__getitem__')


def _is_collection_empty(collection: Iterable[Any]) -> bool:
    try:
        first = next(collection.__iter__())
        return False
    except StopIteration:
        return True


def _predicate_left_func_and_right_str(join_definition: QjoinJoin, elt_left: Any, elt_right: Any):
    return
