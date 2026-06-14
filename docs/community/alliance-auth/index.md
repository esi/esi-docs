---
search:
  exclude: true

title: Alliance Auth
type: service
description: A flexible authentication platform for EVE Online to help in-game organizations manage access to applications and services. AA provides both, a stable core, and a robust framework for community development and custom applications.
maintainer:
  name: Alliance Auth Team
  gitlab: allianceauth
---

# Alliance Auth 

A flexible authentication platform for EVE Online to help in-game organizations manage access to applications and services. AA provides both, a stable core, and a robust framework for community development and custom applications.

[![Version](https://img.shields.io/pypi/v/allianceauth)](https://pypi.org/project/allianceauth/)
[![Python Versions](https://img.shields.io/pypi/pyversions/allianceauth)](https://pypi.org/project/allianceauth/)
[![Django Versions](https://img.shields.io/pypi/djversions/allianceauth)](https://pypi.org/project/allianceauth/)
[![License](https://img.shields.io/badge/license-GPLv2-green)](https://pypi.org/project/allianceauth/)
[![Pipeline Status](https://gitlab.com/allianceauth/allianceauth/badges/master/pipeline.svg)](https://gitlab.com/allianceauth/allianceauth/pipelines)
[![Test Coverage](https://gitlab.com/allianceauth/allianceauth/badges/master/coverage.svg)](https://gitlab.com/allianceauth/allianceauth/pipelines)
[![Documentation Status](https://readthedocs.org/projects/allianceauth/badge/?version=latest)](https://allianceauth.readthedocs.io/en/latest/?badge=latest)
[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

![Alliance Auth](auth-logo.svg)

<div class="grid cards" markdown>

- [:simple-discord: __Discord__](https://discord.gg/fjnHAmk){ .esi-card-link }
- [:simple-gitlab: __GitLab__](https://gitlab.com/allianceauth/allianceauth){ .esi-card-link }
- [:octicons-browser-16: __Documentation__](https://allianceauth.readthedocs.io/){ .esi-card-link }

</div>

## Description

Alliance Auth (AA) is a platform that helps Eve Online organizations efficiently manage access to applications and services.

## Features

- Automatically grants or revokes user access to external services (e.g. Discord, Mumble) and web apps (e.g. SRP requests) based on the user's current membership to [in-game organizations](https://allianceauth.readthedocs.io/en/latest/features/core/states.html) and [groups](https://allianceauth.readthedocs.io/en/latest/features/core/groups.html)
- Provides a central web site where users can directly access web apps (e.g. SRP requests, Fleet Schedule) and manage their access to external services and groups.
- Includes a set of connectors (called ["services"](https://allianceauth.readthedocs.io/en/latest/features/services/)) for integrating access management with many popular external applications / services like Discord, Mumble, Teamspeak 3, SMF and others
- Includes a set of web [apps](https://allianceauth.readthedocs.io/en/latest/features/apps/) which add many useful functions, e.g.: fleet schedule, timer board, SRP request management, fleet activity tracker
- Can be easily extended with additional services and apps. Many are provided by the community and can be found here: [Community Creations](https://gitlab.com/allianceauth/community-creations)
- English :flag_gb:, Chinese :flag_cn:, German :flag_de:, Spanish :flag_es:, Korean :flag_kr:, Russian :flag_ru:, Italian :flag_it:, French :flag_fr:, Japanese :flag_jp: and Ukrainian :flag_ua: Localization

For further details about AA - including an installation guide and a full list of included services and plugin apps - please see the [official documentation](https://allianceauth.rtfd.io).

## Screenshot

Here is an example of the Alliance Auth web site with a mixture of Services, Apps and Community Creations enabled:

### Flatly Theme

![Flatly Theme](SampleInstallation-Flatly.png)

### Darkly Theme

![Darkly Theme](SampleInstallation-Darkly.png)

## Alliance Auth Community Creations

- Over 100+ Applications from 30+ Developers

<https://gitlab.com/allianceauth/community-creations>
