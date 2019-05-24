# ESI Documentation
ESI is the name of EVE Online's publicly available API, allowing you to query the game itself to get info about your character, corporation and more. This documentation can be used as a jumping off point to learn how to begin developing against ESI or as a place to learn some of the ESI concepts that are harder to grasp.

This repo replaces [https://github.com/ccpgames/eveonline-third-party-documentation](https://github.com/ccpgames/eveonline-third-party-documentation), which used to be used for all documentation surrounding EVE Online third party development and the relevant resources from that repository have been moved to this one. Thank you to all who helped maintain it.

We appreciate help from the EVE Online community and encourage pull requests if you feel any documentation is missing. Our wonderful [ESI community](https://github.com/esi/esi-issues/blob/master/contributors.md#esi-community-members) helps to moderate this documentation.

## Important Online Resources
The following is a list of important online resources for ESI development.

* Watch the [third party developer blog](https://developers.eveonline.com/blog) for updates about ESI.
* Make bug or feature requests at our [esi-issues](https://github.com/esi/esi-issues) Github page.
* For real time discussion about ESI join us on our #esi channel in Slack by following [these instructions](https://www.fuzzwork.co.uk/tweetfleet-slack-invites/).
* Watch the [ESI changelog](https://github.com/esi/esi-issues/blob/master/changelog.md) for upcoming endpoint changes. Updates are broadcast in the #esi channel, or you can [subscribe to email notifications](https://app.github-file-watcher.com/?repository=esi/esi-issues&glob=changelog.md).

## Table of Contents
If you're adding a new document, please be sure to include a link here somewhere.

### General

- [ESI Introduction](docs/esi_introduction.md)
- [Frequently Asked Questions](docs/FAQ.md)
- [Transitioning from XML](docs/XML_to_ESI.md)
- [Transitioning from CREST](docs/CREST_to_ESI.md)
- [What defines a breaking change](docs/breaking_changes.md)
- [Warning headers explained](docs/warning_header.md)

### Using ESI Data

- [Dogma](docs/dogma.md)
- [ID Ranges](docs/id_ranges.md)
- [Useful Formulae](docs/useful_formulae.md)
- [Asset location_id](docs/asset_location_id.md)
- [Notifications](docs/notifications.md)

### SSO - Read this notice first!
The documentation below is for the v2 SSO. While it offers several features not available in the v1 SSO, and is going to eventually replace it, it still has some [ongoing issues](https://github.com/ccpgames/sso-issues/issues). It is preferred your application use v2 SSO routes going forward but it may be the case that v2 is not stable enough for your application. If that is the case you can refer to the [old SSO documentation](https://github.com/ccpgames/eveonline-third-party-documentation/blob/master/docs/sso/index.md) for instructions on using the v1 routes.

- [Introduction](docs/sso/README.md)
- [High level overview of SSO authorization flow](docs/sso/sso_authorization_flow.md)
- [Creating an EVE Online SSO application](docs/sso/creating_sso_application.md)
- [OAuth 2.0 for web based applications](docs/sso/web_based_sso_flow.md)
- [OAuth 2.0 for desktop/mobile applications](docs/sso/native_sso_flow.md)
- [Refreshing access tokens](docs/sso/refreshing_access_tokens.md)
- [Validating EVE SSO JWT tokens](docs/sso/validating_eve_jwt.md)
- [Sending authenticated requests to ESI](docs/sso/sending_esi_auth_request.md)

### Static Data Export

- [SDE Introduction](docs/sde_introduction.md)
- [SDE Conversions](docs/sde_conversions.md)

### Community FAQs

- [Guidelines](docs/guidelines.md)
- [Best Practices](docs/best_practices.md)
- [Quick URL Reference](docs/quick_reference.md)
- [Image Server](docs/image_server.md)
- [Developer License](docs/developer_license.md)
