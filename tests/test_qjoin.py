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
