# Community Services


!!! info "Obligatory disclaimer"

    Please note that the table below contains a list of community services that are not officially supported by CCP Games. We acknowledge the hard work and dedication of the developers who have created these services and give them a soapbox to promote their services. However, we do not endorse or guarantee the services listed below. If you have any questions or concerns about a service listed below, please contact the service creator directly.


| Service Name                                        | Creator                                                                                             |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [Sample Service](./sample-service/index.md)         | [:octicons-mark-github-16: Developer McDeveloperface](https://github.com/@your-username-here)       |


# Submitting a Service

If you would like to list your service here, please submit a pull request to this repository, adding your service to the table above, and creating a sub-page in this directory with more information about your service.

## Requirements

1. Your service must be directly related to EVE Online.
2. Your service adheres to the [EVE Online Developer License Agreement](/license-agreement).
3. Your service must be publicly accessible. :material-information-outline:{ title="No private services, please." }
4. The creator of the service has an account in good standing. :material-information-outline:{ title="Yes, being banned counts as 'not in good standing'." }
5. (Bonus) Your service is open source. :material-information-outline:{ title="This is not a requirement, but a nice-to-have." }

As always, we reserve the right to remove any service from this list at any time for any reason, or decline to add a service to this list.

## Service page template

```markdown title="src/docs/community/your-service-name/index.md"
---
search:
  exclude: true
---

# <Name of your service>

## Description

A brief description of your service.

## Features

A short feature showcase of your service.

## Links

- [:octicons-browser-16: Website](https://example.com)
- [:octicons-mark-github-16: GitHub](https://github.com/esi/esi-docs)
- [:simple-discord: Discord](https://discord.gg/eveonline)
- [:simple-x: Twitter](https://twitter.com/eveonline)
- [:simple-reddit: Reddit](https://reddit.com/r/eve)
```

!!! note "A note about search"

    You might have noticed the search exclusion marker in the template above.
    
    This part is required.

    While we want to keep a list of community services, the primary function of this documentation site is to provide access to information about the EVE Online third-party development ecosystem.
    Adding community services to the search index would dilute the search results and make it harder for developers to find the information they need.

    If a service is deemed to be of particular interest to the community, one of the documentation maintainers may choose to remove this exclusion.

## Adding images to your service page

If you want to add images to your service page, be sure to add them to the same directory as your service page. Please keep the images small and optimized for the web, no larger than 250KB or 1024x768 pixels.
