import dataclasses
from typing import Optional

import pytest

import qjoin


def tests_qjoin_request_on_a_single_collection_is_iterable():
    """
    tests that qjoin request on a single collection is iterable and
    returns the element of the collection set in a list of tuple
    """
    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecraft_global = qjoin.on(spacecrafts)
    for spacecraft, in spacecraft_global:
        assert spacecraft == spacecrafts[0]
        break


def tests_qjoin_all_request_should_return_a_list():
    """
    tests that all on qjoin query on a single collection returns a list and returns the elements of the collection in a list of tuples
    """
    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecraft_global = qjoin.on(spacecrafts).all()
    assert isinstance(spacecraft_global, list)
    assert len(spacecraft_global) == len(spacecrafts)


def tests_qjoin_join_request_should_join_2_collection_on_a_simple_key():
    """
    tests that the join function joins 2 collections on a simple key
    """
    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecraft_properties = [
        {'name': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
        {'name': 'GRAIL (A)', 'launch_mass': 202.4},
        {'name': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'name': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
    ]

    spacecraft_global = qjoin.on(spacecrafts).join(spacecraft_properties, key='name').all()
    assert spacecraft_global[0] == (spacecrafts[0], spacecraft_properties[0])
    assert spacecraft_global[3] == (spacecrafts[3], spacecraft_properties[3])


def tests_qjoin_join_request_should_join_2_collection_on_function():
    """
    tests that the join function joins 2 collections on a function
    """
    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecraft_properties = [
        {'name': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
        {'name': 'GRAIL (A)', 'launch_mass': 202.4},
        {'name': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'name': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
    ]

    spacecraft_global = qjoin.on(spacecrafts).join(spacecraft_properties, key=lambda s: s['name'].lower()).all()
    assert spacecraft_global[0] == (spacecrafts[0], spacecraft_properties[0])
    assert spacecraft_global[3] == (spacecrafts[3], spacecraft_properties[3])


def tests_qjoin_join_request_should_fail_when_there_is_no_key_and_left_right_join():
    """
    tests that the join function joins 2 collections on a function
    """
    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecraft_properties = [
        {'name': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
        {'name': 'GRAIL (A)', 'launch_mass': 202.4},
        {'name': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'name': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
    ]

    try:
        spacecraft_global = qjoin.on(spacecrafts).join(spacecraft_properties).all()
        pytest.xfail('expected ValueError execption because there is no key and no left_right_join')
    except ValueError as exception:
        assert True


def tests_qjoin_join_request_should_use_left_and_right_key_to_join_2_collections():
    """
    tests that the join function joins 2 collections that use different keys using left and right parameters.
    """
    # Assign
    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecraft_properties = [
        {'spacecraft': 'GRAIL (A)', 'launch_mass': 202.4},
        {'spacecraft': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'spacecraft': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
        {'spacecraft': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
    ]

    # Acts
    spacecraft_global = qjoin.on(spacecrafts)\
        .join(spacecraft_properties, left=lambda s: s['name'], right='spacecraft')\
        .all()

    # Assert
    assert len(spacecraft_global) == 5
    assert spacecraft_global[0][0]['name'] == 'Kepler'
    assert spacecraft_global[0][1]['spacecraft'] == 'Kepler'
    assert spacecraft_global[4][0]['name'] == 'Psyche'
    assert spacecraft_global[4][1] == None


def tests_qjoin_join_joins_collection_of_object_with_collection_of_dict():
    """
    tests that the join joins 2 collections of objects
    """
    # Assign
    @dataclasses.dataclass
    class Spacecraft:
        name: str
        cospar_id: Optional[str]
        satcat: Optional[int]

    spacecrafts = [
        Spacecraft(name='Kepler', cospar_id='2009-011A', satcat=34380),
        Spacecraft(name='GRAIL (A)', cospar_id='2011-046', satcat=37801),
        Spacecraft(name='InSight', cospar_id='2018-042a', satcat=43457),
        Spacecraft(name='lucy', cospar_id='2021-093A', satcat=49328),
        Spacecraft(name='Psyche', cospar_id=None, satcat=None),
    ]

    spacecraft_properties = [
        {'spacecraft': 'GRAIL (A)', 'launch_mass': 202.4},
        {'spacecraft': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'spacecraft': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
        {'spacecraft': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
    ]

    # Acts
    spacecraft_global = qjoin.on(spacecrafts)\
        .join(spacecraft_properties, left='name', right='spacecraft')\
        .all()

    # Assert
    assert len(spacecraft_global) == 5
    assert spacecraft_global[0][0].name == 'Kepler'
    assert spacecraft_global[0][1]['spacecraft'] == 'Kepler'
    assert spacecraft_global[4][0].name == 'Psyche'
    assert spacecraft_global[4][1] == None

def tests_qjoin_join_joins_collection_of_tuple_with_collection_of_dict():
    """
    tests that the join joins 2 collections of objects
    """
    # Assign
    spacecrafts = [
        ('Kepler', '2009-011A', 34380),
        ('GRAIL (A)', '2011-046', 37801),
        ('InSight', '2018-042a', 43457),
        ('lucy', '2021-093A', 49328),
        ('Psyche', None, None),
    ]

    spacecraft_properties = [
        {'spacecraft': 'GRAIL (A)', 'launch_mass': 202.4},
        {'spacecraft': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'spacecraft': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
        {'spacecraft': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
    ]

    # Acts
    spacecraft_global = qjoin.on(spacecrafts)\
        .join(spacecraft_properties, left=0, right='spacecraft')\
        .all()

    # Assert
    assert len(spacecraft_global) == 5
    assert spacecraft_global[0][0][0] == 'Kepler'
    assert spacecraft_global[0][1]['spacecraft'] == 'Kepler'
    assert spacecraft_global[4][0][0] == 'Psyche'
    assert spacecraft_global[4][1] == None


def tests_qjoin_as_aggregate_should_consolidate_in_simple_dataclass():
    """
    tests that the join joins 2 collections of objects
    """
    # Assign
    @dataclasses.dataclass
    class Spacecraft:
        spacecraft: dict = dataclasses.field(init=False)
        properties: dict = dataclasses.field(init=False)

    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecraft_properties = [
        {'spacecraft': 'GRAIL (A)', 'launch_mass': 202.4},
        {'spacecraft': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'spacecraft': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
        {'spacecraft': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
    ]

    # Acts
    spacecraft_global = qjoin.on(spacecrafts)\
        .join(spacecraft_properties, left='name', right='spacecraft')\
        .as_aggregate(Spacecraft, ['spacecraft', 'properties'])

    # Assert
    assert len(spacecraft_global) == 5
    assert spacecraft_global[0].properties['power'] == 1100


def tests_qjoin_as_aggregate_should_create_aggregate_without_joins():
    """
    tests that the join joins 2 collections of objects
    """
    # Assign
    @dataclasses.dataclass
    class Spacecraft:
        spacecraft: dict = dataclasses.field(init=False)

    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    # Acts
    spacecraft_global = qjoin.on(spacecrafts)\
        .as_aggregate(Spacecraft, ['spacecraft'])

    # Assert
    assert len(spacecraft_global) == 5
    assert spacecraft_global[0].spacecraft['cospar_id'] == '2009-011A'


def tests_qjoin_as_aggregate_should_execute_post_qjoin_method():
    """
    tests that the join joins 2 collections of objects
    """
    # Assign
    @dataclasses.dataclass
    class Spacecraft:
        name: str = dataclasses.field(init=False)
        spacecraft: dict = dataclasses.field(init=False)
        properties: dict = dataclasses.field(init=False)

        def __post_qjoin__(self):
            self.name = self.spacecraft['name']

    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecraft_properties = [
        {'spacecraft': 'GRAIL (A)', 'launch_mass': 202.4},
        {'spacecraft': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'spacecraft': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
        {'spacecraft': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
    ]

    # Acts
    spacecraft_global = qjoin.on(spacecrafts)\
        .join(spacecraft_properties, left='name', right='spacecraft')\
        .as_aggregate(Spacecraft, ['spacecraft', 'properties'])

    # Assert
    assert len(spacecraft_global) == 5
    assert spacecraft_global[0].name == 'Kepler'


def tests_qjoin_join_joins_on_empty_base_collection():
    """
    tests that the join joins 2 collections of objects
    """
    # Assert
    @dataclasses.dataclass
    class Spacecraft:
        name: str
        cospar_id: Optional[str]
        satcat: Optional[int]

    spacecrafts = []

    spacecraft_properties = [
        {'spacecraft': 'GRAIL (A)', 'launch_mass': 202.4},
        {'spacecraft': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'spacecraft': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
        {'spacecraft': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
    ]

    # Acts
    spacecraft_global = qjoin.on(spacecrafts)\
        .join(spacecraft_properties, left='name', right='spacecraft')\
        .all()

    # Assert
    assert len(spacecraft_global) == 0


def tests_qjoin_join_joins_with_empty_right_collection():
    """
    tests that qjoin join function joins with empty right collection
    """
    # Assert
    @dataclasses.dataclass
    class Spacecraft:
        name: str
        cospar_id: Optional[str]
        satcat: Optional[int]

    spacecrafts = [
        Spacecraft(name='Kepler', cospar_id='2009-011A', satcat=34380),
        Spacecraft(name='GRAIL (A)', cospar_id='2011-046', satcat=37801),
        Spacecraft(name='InSight', cospar_id='2018-042a', satcat=43457),
        Spacecraft(name='lucy', cospar_id='2021-093A', satcat=49328),
        Spacecraft(name='Psyche', cospar_id=None, satcat=None),
    ]

    spacecraft_properties = [
    ]

    # Acts
    spacecraft_global = qjoin.on(spacecrafts)\
        .join(spacecraft_properties, left='name', right='spacecraft')\
        .all()

    # Assert
    assert len(spacecraft_global) == 5
    assert spacecraft_global[0][0].name == 'Kepler'
    assert spacecraft_global[0][1] == None
    assert spacecraft_global[4][0].name == 'Psyche'
    assert spacecraft_global[4][1] == None
