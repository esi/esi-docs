---
search:
  exclude: true

title: EVE Auth for Django
type: resource
description: A Django app for authorizing Django sites with the EVE Online SSO service..
maintainer:
  name: Erik Kalkoken
  github: ErikKalkoken
---

# EVE Auth for Django

A Django app for authorizing Django sites with the EVE Online SSO service.

[![release](https://img.shields.io/pypi/v/django-eve-auth?label=release)](https://pypi.org/project/django-eve-auth/)
[![python](https://img.shields.io/pypi/pyversions/django-eve-auth)](https://pypi.org/project/django-eve-auth/)
[![django](https://img.shields.io/pypi/djversions/django-eve-auth?label=django)](https://pypi.org/project/django-eve-auth/)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/python-eveauth/-/blob/master/LICENSE)

<div class="grid cards" markdown>

- [:octicons-browser-16: **Website**](https://erikkalkoken.github.io/python-eveauth){ .esi-card-link }
- [:octicons-mark-gitlab-16: **GitHub**](https://gitlab.com/ErikKalkoken/django-eve-auth){ .esi-card-link }

</div>

## Features

- Users can login via EVE SSO. New user accounts will automatically be created from the Eve character.
- Users keep their accounts as long as the character does not change ownership
- User's character name is updated with every new login
- Supports Django's default login URLs and next parameter
- Also includes a template tag for creating user icons with the related eve character portrait
- Fully tested

For more information please visit the [GitLab repository](https://gitlab.com/ErikKalkoken/django-eve-auth).
