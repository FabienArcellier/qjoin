Collections
###########

``qjoin`` is able to merge several types of collections together. This page lists those that are supported.

The elements of a collection must respect 2 constraints. Each element must be a container and each element must contain the join key.

Collection of dictionnary
*************************

A dictionary collection can be used both as a base collection and as a join collection.

.. code-block:: python

    spacecrafts = [
        {'name': 'Kepler', 'cospar_id': '2009-011A', 'satcat': 34380},
        {'name': 'GRAIL (A)', 'cospar_id': '2011-046', 'satcat': 37801},
        {'name': 'InSight', 'cospar_id': '2018-042a', 'satcat': 43457},
        {'name': 'lucy', 'cospar_id': '2021-093A', 'satcat': 49328},
        {'name': 'Psyche', 'cospar_id': None, 'satcat': None},
    ]

Dictionaries in the same collection can have a variable number of keys, provided that the join key is always present.

.. code-block:: python

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

Collection of tuple
*******************

A tuple collection can be used as both a base collection and a join collection.

.. code-block:: python

    spacecrafts = [
        ('Kepler', '2009-011A', 34380),
        ('GRAIL (A)', '2011-046', 37801),
        ('InSight', '2018-042a', 43457),
        ('lucy', '2021-093A', 49328),
        ('Psyche', None, None),
    ]

.. code-block:: python

    global_space_crafts = qjoin.on(spacecrafts).join(spacecrafts_properties, left=0, right='name').all()
    for spacecraft, spacecraft_properties in global_space_crafts:
        print(spacecraft[0])

Collection of list
******************

A list collection can be used as both a base collection and a join collection.

.. code-block:: python

    spacecrafts = [
        ['Kepler', '2009-011A', 34380],
        ['GRAIL (A)', '2011-046', 37801],
        ['InSight', '2018-042a', 43457],
        ['lucy', '2021-093A', 49328],
        ['Psyche', None, None],
    ]

.. code-block:: python

    global_space_crafts = qjoin.on(spacecrafts).join(spacecrafts_properties, left=0, right='name').all()
    for spacecraft, spacecraft_properties in global_space_crafts:
        print(spacecraft[0])

Collection of objects
*********************

A collection of objects can be used both as a base collection and as a join collection.

.. code-block:: python

    class Spacecraft:
        def __init__(self, name, cospar_id, satcat):
            self.name = name
            self.cospar_id = cospar_id
            self.satcat = satcat

    spacecrafts = [
        Spacecraft('Kepler', '2009-011A', 34380),
        Spacecraft('GRAIL (A)', '2011-046', 37801),
        Spacecraft('InSight', '2018-042a', 43457),
        Spacecraft('lucy', '2021-093A', 49328),
        Spacecraft('Psyche', None, None),
    ]

.. code-block:: python

    global_space_crafts = qjoin.on(spacecrafts).join(spacecrafts_properties, left='name', right='name').all()
    for spacecraft, spacecraft_properties in global_space_crafts:
        print(spacecraft.name)

.. note::

    qjoin supporte les collections d'objets qui viennent d'ORM comme ``sqlalchemy`` ou ``django``.
