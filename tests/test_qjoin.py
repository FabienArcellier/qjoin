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
