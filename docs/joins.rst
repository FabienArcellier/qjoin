Joins
#####

This page explores the different joins possible with ``qjoin``.

.. contents::
  :backlinks: top

A join defines how a base collection and a join collection will be related together. It always applies between 2 collections. A qjoin query can consist of one or more joins.

Simple joins
============

To do a simple join, the base collection and the joining collection must share an attribute in common.

.. code-block:: python

    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecrafts_mission_infos = [
        {'name': 'Kepler', 'mission_type': 'Space telescope', 'launch_date':'2009-03-07T03:49Z', 'end_of_mission': '2018-11-15'},
        {'name': 'GRAIL (A)', 'launch_date':'2011-09-10T13:08Z', 'end_of_mission': '2012-12-17'},
        {'name': 'InSight', 'mission_type': 'Mars lander', 'launch_date':'2018-05-05T11:05Z', 'end_of_mission': '2022-12-21'},
        {'name': 'lucy', 'mission_type': 'Multiple-flyby of asteroids', 'launch_date':'2021-10-16T09:34Z'},
    ]

.. code-block:: python

    global_space_crafts = qjoin.on(spacecrafts).join(spacecrafts_mission_infos, key='name').all()
    for spacecraft, spacecraft_mission_infos in global_space_crafts:
        print(spacecraft['name'])


Left right joins using simple key
=================================

If the join is done on different attributes between the base collection and the join collection, then a left-right join will be necessary.

.. code-block:: python

    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecrafts_mission_infos = [
        {'mission': 'Kepler', 'mission_type': 'Space telescope', 'launch_date':'2009-03-07T03:49Z', 'end_of_mission': '2018-11-15'},
        {'mission': 'GRAIL (A)', 'launch_date':'2011-09-10T13:08Z', 'end_of_mission': '2012-12-17'},
        {'mission': 'InSight', 'mission_type': 'Mars lander', 'launch_date':'2018-05-05T11:05Z', 'end_of_mission': '2022-12-21'},
        {'mission': 'lucy', 'mission_type': 'Multiple-flyby of asteroids', 'launch_date':'2021-10-16T09:34Z'},
    ]

.. code-block:: python

    global_space_crafts = qjoin.on(spacecrafts) \
                               .join(spacecrafts_mission_infos, left='name', right='mission') \
                               .all()

    for spacecraft, spacecraft_mission_infos in global_space_crafts:
        print(spacecraft['name'])

Joins using artificial key
===========================

If it is necessary to transform the keys to be able to make a join between the base collection and the joining collection, then it will be necessary to make a join from an artificial key.

.. code-block:: python

    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecrafts_mission_infos = [
        {'mission': 'KEPLER', 'mission_type': 'Space telescope', 'launch_date':'2009-03-07T03:49Z', 'end_of_mission': '2018-11-15'},
        {'mission': 'GRAIL (A)', 'launch_date':'2011-09-10T13:08Z', 'end_of_mission': '2012-12-17'},
        {'mission': 'INSIGHT', 'mission_type': 'Mars lander', 'launch_date':'2018-05-05T11:05Z', 'end_of_mission': '2022-12-21'},
        {'mission': 'LUCY', 'mission_type': 'Multiple-flyby of asteroids', 'launch_date':'2021-10-16T09:34Z'},
    ]

.. code-block:: python

    global_space_crafts = qjoin.on(spacecrafts) \
                               .join(spacecrafts_mission_infos, left=lambda l: l['name'].lower(), right=lambda l: l['mission'].lower()) \
                               .all()

    for spacecraft, spacecraft_mission_infos in global_space_crafts:
        print(spacecraft['name'])


Multiple join
=================

Multiple joins with multiple join collections can be composed on a single ``qjoin`` query.

.. code-block:: python

    spacecrafts = [.join(countries, left='country', right='name')
    .join(countries, left='birth_country', right='name')
    .all()
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

    spacecrafts_mission_infos = [
        {'mission': 'Kepler', 'mission_type': 'Space telescope', 'launch_date':'2009-03-07T03:49Z', 'end_of_mission': '2018-11-15'},
        {'mission': 'GRAIL (A)', 'launch_date':'2011-09-10T13:08Z', 'end_of_mission': '2012-12-17'},
        {'mission': 'InSight', 'mission_type': 'Mars lander', 'launch_date':'2018-05-05T11:05Z', 'end_of_mission': '2022-12-21'},
        {'mission': 'lucy', 'mission_type': 'Multiple-flyby of asteroids', 'launch_date':'2021-10-16T09:34Z'},
    ]

    spacecraft_properties = [
        {'name': 'Kepler', 'dimension': (4.7, 2.7, None), 'power': 1100, 'launch_mass': 1052.4},
        {'name': 'GRAIL (A)', 'launch_mass': 202.4},
        {'name': 'InSight', 'dimension': (6, 1.56, 1), 'power': 600, 'launch_mass': 694},
        {'name': 'lucy', 'dimension': (13, None, None), 'power': 504, 'launch_mass': 1550},
    ]

.. code-block:: python

    global_space_crafts = qjoin.on(spacecrafts) \
                               .join(spacecrafts_mission_infos, left='name', right='mission') \
                               .join(spacecraft_properties, key='name') \
                               .all()

    for spacecraft, spacecraft_mission_infos, spacecraft_property in global_space_crafts:
        print(spacecraft['name'])

Multiple join on the same join collection
=========================================

Multiple joins on a single join collection can be composed on a single ``qjoin`` query.

.. code-block:: python

    persons = [
        {'name': 'John', 'age': 25, 'country': 'USA', 'birth_country': 'USA'},
        {'name': 'Paul', 'age': 18, 'country': 'UK', 'birth_country': 'USA'},
        {'name': 'Ringo', 'age': 20, 'country': 'UK', 'birth_country': 'UK'},
        {'name': 'George', 'age': 22, 'country': 'UK', 'birth_country': 'Japan'},
        {'name': 'Yoko', 'age': 30, 'country': 'Japan', 'birth_country': 'Japan'},
    ]

    countries = [
        {'name': 'USA', 'continent': 'America'},
        {'name': 'UK', 'continent': 'Europe'},
        {'name': 'Japan', 'continent': 'Asia'},
    ]

.. code-block:: python

    persons_with_country_infos = qjoin.on(persons) \
                               .join(countries, left='country', right='name') \
                               .join(countries, left='birth_country', right='name') \
                               .all()

    for person, country, birth_country in persons_with_country_infos:
        print(person['name'])

