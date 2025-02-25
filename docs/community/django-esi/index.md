---
search:
  exclude: true

title: Django-ESI
type: resource
description: Django app for easy access to the EVE Swagger Interface (ESI)
maintainer:
  name: Alliance Auth Team
  gitlab: allianceauth
---

# Django-ESI

Django app for easy access to the EVE Swagger Interface (ESI)

[![Version](https://img.shields.io/pypi/v/django-esi)](https://pypi.org/project/django-esi/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-esi)](https://pypi.org/project/django-esi/)
[![Django Versions](https://img.shields.io/pypi/djversions/django-esi)](https://pypi.org/project/django-esi/)
[![License](https://img.shields.io/badge/license-GPLv3-green)](https://pypi.org/project/django-esi/)
[![Pipeline Status](https://gitlab.com/allianceauth/django-esi/badges/master/pipeline.svg)](https://gitlab.com/allianceauth/django-esi/pipelines)
[![Test Coverage](https://gitlab.com/allianceauth/django-esi/badges/master/coverage.svg)](https://gitlab.com/allianceauth/django-esi/pipelines)
[![Documentation Status](https://readthedocs.org/projects/django-esi/badge/?version=latest)](https://django-esi.readthedocs.io/en/latest/?badge=latest)
[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

<div class="grid cards" markdown>

- [:simple-discord: __Discord__](https://discord.gg/fjnHAmk){ .esi-card-link }
- [:simple-gitlab: __GitLab__](https://gitlab.com/allianceauth/django-esi){ .esi-card-link }
- [:octicons-browser-16: __Documentation__](https://django-esi.readthedocs.io/en/latest/){ .esi-card-link }

</div>

## Description

Django-esi is a Django app that provides an interface for easy access to the EVE Swagger Interface (ESI), the official API for the game [EVE Online](https://www.eveonline.com/).

It is build upon [Bravado](https://github.com/Yelp/bravado) - a python client library for Swagger 2.0 services.

Django-esi adds the following main functionalities to a Django site:

- Dynamically generated client for interacting with public and private ESI endpoints
- Support for adding EVE SSO to authenticate characters and retrieve tokens
- Control over which ESI endpoint versions are used
