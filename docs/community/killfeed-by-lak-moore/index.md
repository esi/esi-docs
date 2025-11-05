---
search:
  exclude: true

title: KillFeed by Lak Moore
type: service
description: Discord bot to post filtered killmails from the Massively Multiplayer Online Role Playing Game (MMORPG) EVE-Online using data from zKillboard and Janice.
maintainer:
  name: Lak Moore
  github: LakMoore
---

# KillFeed by Lak Moore

Eve Online zKillboard Discord Bot.

<div class="grid cards" markdown>

- [:octicons-mark-github-16: __GitHub__](https://github.com/LakMoore/KillFeed){ .esi-card-link }
- [:simple-discord: __Discord__](https://discord.gg/m4pyj2q8X9){ .esi-card-link }

</div>

## About

Use the Discord link below to add the bot to your Discord server and use the simple commands to apply filters of interest.  The bot will then post matching killmails from zKillboard.com into that Discord channel.

[Add the bot to your server](https://discord.com/api/oauth2/authorize?client_id=1041057662432968745&permissions=2048&scope=applications.commands%20bot)

| Command      | Description                                                                                                                                                                                                       |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /init        | Intialise the channel and set up the bot, needs Send Message and Manage Message permissions.  Note: the bot does not have Read Permissions on messages so cannot read any messages in any channel on your server. | 
| /add         | Add a rule to the filter in this channel.                                                                                                                                                                         |
| /remove      | Remove a rule from the filter in this channel.                                                                                                                                                                    |
| /show        | Choose whether to show Killmails, Lossmails or both.                                                                                                                                                              |
| /filter_mode | Choose whether to apply boolean OR or AND to the filters in this channel.                                                                                                                                         |
| /min_isk     | Only show results above a minimum value in ISK.                                                                                                                                                                   |

Filters available include:

 - Character
 - Corporation
 - Alliance
 - Ship Type
 - Region
 - Constellation
 - System
 - Minimum ISK value
 - Kill/Loss/All

Filters can be ANDed or ORed to capture everything or fine tune your requirements.

Current bot stats (as at 19th October 2025):

 - Serving KillMails on 66 servers.
 - First server stats recorded 2 years ago
 - Polled zKill 13,381,362 times
 - Received 11,078,460 killmails from zKill
 - Posted 19,675,183 killmails into Discord
 - Appraised 1,792,910.6B ISK with Janice

Join the [KillFeed by Lak Moore Discord](https://discord.gg/m4pyj2q8X9) for support and feature requests.
