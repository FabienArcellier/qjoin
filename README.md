## qjoin

[![ci](https://github.com/FabienArcellier/qjoin/actions/workflows/main.yml/badge.svg)](https://github.com/FabienArcellier/qjoin/actions/workflows/main.yml)
[![Documentation Status](https://readthedocs.org/projects/qjoin/badge/?version=latest)](https://qjoin.readthedocs.io/en/latest/?badge=latest)

**Work in progress ..., everything has to be implemented**

qjoin is a data manipulation library that provides simple and efficient joining and collection processing functionality. It simplifies and optimizes the process of joining different entities and provides methods for aggregating, organizing, and sorting data.

![principle diagram](docs/principle.png)

* qjoin is a simple and efficient way to join and process data
* qjoin is a steroid extension of the `zip` function in python
* qjoin works on all iterators, whether lists of dictionaries, objects or sqlalchemy or django models

## Project links

* PyPI Releases
* [Documentation](https://qjoin.readthedocs.io/en/latest/)
* [Source code](https://github.com/FabienArcellier/qjoin)
* [Issue tracker](https://github.com/FabienArcellier/qjoin/issues)
* [Chat](https://discord.gg/nMn9YPRGSY)

## Installation

```bash
pip install qjoin
```

## Usage

Here are examples of how qjoin will be used in the future.

```python
# Basic usage
qjoin.on(persons).join(cities, key="city").all()

person_infos = qjoin.on(persons).join(cities, left="city", right="city").all()
for person, city in person_infos:
    print(f'{person} - {city}')

person_infos = qjoin.on(persons) \
    .join(cities, left=lambda p: p.city, right=lambda c: c.city) \
    .join(cars, left=lambda p: p.car, right=lambda c: c.car) \
    .all()

for person, city, car in person_infos:
    print(f'{person} - {city} - {car}')

qjoin.on(persons) \
    .join(cities, left=lambda p: p.city, right=lambda c: c.city) \
    .sort(lambda p, c: p.name) \
    .all()

# Advanced transformation

qjoin.on(persons) \
    .join(cities, left=lambda p: p.city, right=lambda c: c.city) \
    .join(cars, left=lambda p: p.car, right=lambda c: c.car) \
    .as_aggregate(Aggregate, lambda p, ci, ca: Aggregate(p, ci, ca))

qjoin.on(persons) \
    .join(cities, left=lambda p: p.city, right=lambda c: c.city) \
    .join(cars, left=lambda p: p.car, right=lambda c: c.car) \
    .as_aggregate(Aggregate, ['person', 'city', 'cars'])


qjoin.on(persons) \
    .join(cities, left=lambda p: p.city, right=lambda c: c.city) \
    .as_lookup(lambda p: p.name)

qjoin.on(persons) \
    .join(cities, left=lambda p: p.city, right=lambda c: c.city) \
    .as_multilookup(lambda p, c: c.city

# Advanced

qjoin.on(persons) \
    .join(cities, left=lambda p: p.city, right=lambda c: c.city, scan_strategy=qjoin.RIGHT_LOOKUP)
    .join(cars, left=lambda p: p.car, right=lambda c: c.car, default=Car(car='unknown', constructor='unknown')) \
    .as_aggregate(Aggregate, lambda p, ci, ca: Aggregate(p, ci, ca))
```

### Try with docker

You can run this template with docker. The manufactured image can be distributed and used to deploy your application to a production environment.

```bash
docker-compose build
docker-compose run app
```

### Try with gitpod

[gitpod](https://www.gitpod.io/) can be used as an IDE. You can load the code inside to try the code.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/FabienArcellier/qjoin.git)

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/qjoin.git
```

## Contributing

**This library has to be implemented. If you want to discuss about it, contact me through [discord](https://discord.gg/nMn9YPRGSY).**

Contributing to this project is done through merge request (pull request in github). You can contribute to this project by discovering bugs, opening issues or submitting merge request.

more in [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT License

Copyright (c) 2023-2023 Fabien Arcellier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
