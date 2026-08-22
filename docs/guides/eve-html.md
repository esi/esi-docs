# EVE HTML

Wherever text in EVE can be formatted — a mail, a character bio, a corporation description, an item's description — it is stored as a small HTML-like markup, and ESI hands it back to you exactly as it is stored.
It looks close enough to HTML that passing it straight to an HTML renderer almost works, which is the trap.

The format has no official name.
Third-party developers call it *EVE HTML*, *EVE-flavored HTML* or *EVE formatted text*, and the links inside it *chat links* or *in-game links*.

## Where you will find it

| Source | Field |
| ------ | ----- |
| `/characters/{character_id}/mail/{mail_id}` | `body` |
| `/characters/{character_id}` | `description` (the character's bio) |
| `/corporations/{corporation_id}` | `description` |
| `/characters/{character_id}/calendar/{event_id}` | `text` |
| `/universe/types/{type_id}`, and `types.yaml` in the [SDE](../services/static-data/index.md) | `description` |

Assume any player-written or CCP-written prose that ESI returns may contain it: faction descriptions, NPC corporation descriptions and dogma attribute descriptions all carry it too.
ESI's own example response for a calendar event is a good illustration of how ordinary it is:

```
o7: The EVE Online Show features latest developer news […] on <a href="http://www.twitch.tv/ccp">EVE TV</a>. Don't miss it!
```

The same markup is what the client puts on your clipboard when a player copies a chat message, and what the client accepts back when you write a mail — see [Writing EVE HTML](#writing-eve-html).

Two places it is *not*: alliances have no description field in ESI at all, and the `text` of a notification is YAML rather than this markup.

## What it looks like

This is the start of the description of PLEX (type 44992), verbatim from the SDE:

```
PLEX is an item that can be traded between players on the regional market. PLEX can also be
used in the New Eden Store to upgrade your account to Omega Clone State, purchase virtual
goods, and activate other account services.

<font size="14"><b>Getting PLEX</b></font>
PLEX can be purchased on the regional market for ISK, from the PLEX Vault, or securely on
<url=https://secure.eveonline.com/PLEX/>https://secure.eveonline.com/PLEX/</url> using a
variety of methods.

<font color="#ff3399cc">TIP: Purchasing PLEX to sell for ISK to other players is a great way
to kickstart your capsuleer career!</font>
[…]
```

The line breaks above are literal `\r\n` in the data, not `<br>` tags, and each paragraph is a single long line — they are wrapped here for readability.

That is the tidy end of the format. Here is the messy end — the client's own location label, as the UI holds it:

```
<url=showinfo:5//30000142 alt='Current Solar System'>Jita</url></b> <color=0xff4cffccL><hint='Security status'>0.9</hint></color><fontsize=12><fontsize=8> </fontsize>&lt;<fontsize=8> </fontsize><url=showinfo:4//20000020>Kimotoro</url><fontsize=8> </fontsize>&lt;<fontsize=8> </fontsize><url=showinfo:3//10000002>The Forge</url>
```

In that one line: a `</b>` closing a tag that was never opened, a link carrying an extra `alt` attribute, a color value with a stray `L` on the end, `&lt;` standing in for a literal `<`, and `<fontsize=8>` used to make a narrow space.
Almost everything on this page is somewhere in there.

So be lenient — much more lenient than you would be with HTML.
Tags go missing, closing tags turn up with nothing open, and open and close tags cross each other: `<b><i></b></i>` is not a typo, it is ordinary. Anything that expects well-formed markup falls over on everyday data.

## It is not HTML

It borrows angle brackets and little else.

- **The tag set is tiny and fixed.** Some inline formatting, a line break, a link and a few layout markers. No document structure, no stylesheet, no `class`.
- **Links do not point at web pages.** An `href` normally carries a custom URI scheme such as `showinfo:` naming an in-game window. A browser does nothing useful with it.
- **The markup is frequently malformed, including in CCP's own data.** The SDE's English type descriptions alone hold 42 unclosed `<i>` tags, 6 unclosed `<font>` tags, 56 `<p>` elements that never close, and a dozen `</b>` tags with nothing to close.
- **Attributes are usually unquoted.** In those same descriptions `href` appears without quotes 2,108 times and with quotes 5 times, so a renderer that rewrites strings on the assumption of `attr="value"` gets the common case wrong.

To see why an HTML parser is the wrong tool, hand a browser `<url=showinfo:5//30000142>Jita</url>`.
It produces an element named `url=showinfo:5` with an attribute called `30000142`, and since `</url>` does not close *that*, the entire rest of the message becomes its child.
A sanitizer that drops unknown elements along with their contents then deletes the mail.

Write, or borrow, a tolerant tokenizer — [Parsing](#parsing) shows one.

## The client's parser

The format has never been specified, but the client's parser for it is public.
CCP open-sourced the Carbon rendering engine, and `Tr2LabelTextParser.cpp` in [carbonengine/trinity](https://github.com/carbonengine/trinity/blob/main/trinity/Tr2LabelTextParser.cpp) is the tokenizer behind the UI's `Label`, exposed to the client's Python as `blue.ParseLabelText` and described there as:

> This is used by the UI's Label to parse our custom HTML-ish language very quickly.
> It is almost surely not useful for any other purpose.

Everything below about *what the client accepts* comes from that file.
It is the closest thing to a specification that exists, with one caveat: it is the label parser, and text also passes through the client's localization layer, which is not public.
What your application should then *do* with the result is a separate question, answered by the sections after it.

!!! note "Crowdsourced"
    The link schemes further down are not in the parser — they are payloads the UI hands to other code — so that list is what third-party parsers have run into rather than anything complete.
    If you know a scheme, tag or field this page is missing, please open a pull request.

## Lexical structure

A document is a flat sequence of literal text and tags.
There is no root element, no declaration, and no requirement that tags nest.

### Tag syntax

Tag names are case-insensitive, and mixed case does occur — the SDE contains `<br>`, `<BR>` and `<Br>`.

Tags that take no attributes must be written exactly, with no whitespace inside them: `<b>` is bold, `<b >` is an unknown tag.
`<br>` is the exception, and tolerates spaces, tabs and `&nbsp;` before its `>` or `/>`.

### Attributes

Attributes come in three shapes, and all three occur in official data:

| Shape | Example (verbatim from the SDE) | Notes |
| ----- | ------------------------------- | ----- |
| Unquoted attribute | `<a href=showinfo:34>Tritanium</a>` | The most common form. Ends at a space, a tab, a `>` or an `&nbsp;`, so the value cannot contain a space |
| Quoted attribute | `<font size="14"><b>Getting PLEX</b></font>` | Single quotes work too: `<color='0xFF33FFFF'>1.0</color>` |
| Tag value | `<url=showinfo:2//1000125>CONCORD</url>` | The tag carries one value instead of named attributes |

In the SDE's English type descriptions, `href` appears without quotes 2,108 times and with quotes 5 times. Mail written by the in-game editor quotes far more often.

The third shape — CCP's source calls it an *attribtag* — has no HTML equivalent and is easy to miss.
Five tags take it: `<color=…>`, `<fontsize=…>`, `<hint=…>`, `<letterspace=…>` and `<url=…>`.
Read the value as an attribute named after the tag itself; `<url=…>` and `<a href="…">` then express the same link in the same way.
Ordinary attributes may follow the value inside the same tag — the client writes `<url=showinfo:5//30000142 alt='Current Solar System'>`, where `alt` is a tooltip.

Two more details catch parsers out: `&nbsp;` counts as whitespace *between* attributes, and attribute names keep the case they were written in, so `<a HREF=…>` gives you a key of `HREF`.
If the attribute list does not parse, the client discards the tag *and* everything up to the next `>` after it — a malformed `<font size>text</font> more` renders as just ` more` — or throws away the rest of the string if there is no later `>`.

### Text, entities and whitespace

Exactly four character entities are decoded, case-insensitively:

| Entity | Becomes |
| ------ | ------- |
| `&amp;` | `&` |
| `&lt;` | `<` |
| `&gt;` | `>` |
| `&nbsp;` | An ordinary space, not U+00A0 |

Nothing else is. `&quot;`, `&apos;` and numeric entities such as `&#39;` stay as literal text.

Whitespace is significant — there is no HTML-style collapsing of runs of spaces, and players use runs of spaces to line up columns in their corporation descriptions.
A literal tab character is replaced with a single space.

Line breaks come from `<br>`, from a literal `\n` and from a literal `\r\n`. A lone `\r` does not break the line — the client leaves it in the text as an ordinary character.
CCP's own type descriptions use `\r\n` in some places and `<br><br>` in others.

### Unknown tags, and the stray `<`

An unrecognized tag is not rendered as text.
The client discards everything from the `<` to the next `>` — and if there is no later `>` **it stops parsing and throws away the rest of the string**.

That is not a rare edge case.
A player who types `<3` in their bio loses the text between it and the next `>` — and if nothing later in the bio has one, the rest of the bio.
Most third-party renderers are friendlier and treat a `<` that does not begin a valid tag as literal text, which is a reasonable choice as long as you know you are diverging from the client.

## Tags

These are the tags the client recognizes.

| Tag | Closing tag | Effect |
| --- | ----------- | ------ |
| `<b>` | `</b>` | Bold |
| `<i>` | `</i>` | Italic |
| `<u>` | `</u>` | Underline |
| `<uppercase>` | `</uppercase>` | Upper-cases the enclosed text |
| `<br>` | — | Line break. `<br/>` is accepted. `</br>` occurs in CCP's data but does nothing |
| `<font size=… color=…>` | `</font>` | Font size and color |
| `<fontsize=…>` | `</fontsize>` | Font size only |
| `<color=…>` | `</color>` | Color only |
| `<letterspace=…>` | `</letterspace>` | Letter spacing |
| `<a href=…>` | `</a>` | Link — see [Links](#links) |
| `<url=…>` | `</url>` | Link. The legacy spelling `<url:…>` is rewritten to `<url=…>` before parsing |
| `<hint=…>` | `</hint>` | Tooltip text |
| `<localized hint=…>` | `</localized>` | A name in two languages — see below |
| `<left>`, `<right>`, `<center>` | — | Line alignment. These have no closing tags |
| `<t>` | — | Column separator. Splits the line into tab stops rather than styling anything |

Most of that list is for the client's own UI. What you will actually meet in ESI data is a much smaller set: `<b>`, `<i>`, `<u>`, `<br>`, `<font>`, `<color=…>`, `<a>` and `<url=…>`, with `<localized>` showing up in text a client has copied to the clipboard.

Anything not in the table is an unknown tag, including several that turn up in real ESI data: `<loc>`, `<p>`, `<div>`, `<ul>` and `<li>`.
`<loc>` is the odd one. The label parser does not know it, which suggests it is a marker for the localization layer rather than something the renderer acts on. It is rare in the SDE — eight occurrences, all on one type — and never closed there, but corporation descriptions from the live API do close it, so handle `</loc>` as well.

Drop the tag and keep its contents.
That is the right default for any tag you do not recognize: an unknown tag then costs you some styling instead of a chunk of the message.

### Font size

`size` is an integer.
The client's font stack sizes glyphs in pixels — it hands the value to FreeType with the pixel-size flag — so read it as a pixel height rather than a point size or an HTML `size="1..7"` bucket, which would render `size="14"` at the browser's largest.
The client applies its own UI scaling on top, and no default size is published, so scale rather than copy: pick your own body size — 12 is a reasonable stand-in — and render at `size / 12` of it. Clamp both ends. CCP's `size="2"` fine print is legible in game and is not at 2px, and a third-party tool's `size="30"` headline will blow out your layout.

CCP's type descriptions use only `size="14"` for headings and `size="2"` for fine print.
Mail written by third-party tools ranges wider: [RIFT](../community/rift-intel-fusion-tool/index.md) generates `size="30"` headlines and `size="12"` small print.

### `<localized>`

`<localized hint="…">…</localized>` wraps a name that exists in more than one language.
The tag is in the client's parser, but it does not appear anywhere in the SDE — where third-party developers actually run into it is [XML fitting exports](fitting.md#xml) from a localized client, which is how it broke a generation of fitting importers.

```
<localized hint="Vexor">Vexor*</localized>
```

Render the contents — that is what the client displays — and use the `hint` as a tooltip.
A trailing asterisk marks a name the client had no translation for.
Which language ends up on which side depends on the client that produced the text, so do not rely on one of them being English.

If you have a captured example from a non-English client, it would be a useful thing to contribute.

## Colors

A color is written in one of three forms, all of which occur in the SDE:

| Form | Example | Notes |
| ---- | ------- | ----- |
| `0xAARRGGBB` | `0xFF33FFFF` | Eight hex digits, in any case |
| `#AARRGGBB` | `#ff3399cc` | Same value, different prefix |
| Named | `yellow` | An undocumented set of names |

!!! warning "Alpha comes first"
    CSS's eight-digit hex color is `#RRGGBBAA`. EVE's is `#AARRGGBB`.
    Handing an EVE color to a browser unchanged silently gives you a different color: `#ff0000ff` is opaque **blue** in EVE and opaque **red** in CSS, and `#80ff0000` is half-transparent **red** in EVE but invisible **yellow-green** in CSS.
    Split the value yourself — first two digits alpha, remaining six the color.

A value can also carry a trailing `L` — `0xff4cffccL` — a Python long-integer literal that has leaked through. Strip it before parsing.

Alpha is usually `ff`, but not always — the client's own default body text is `#bfffffff`, white at 75%.
Dropping a leading `ff` and using the remaining `#RRGGBB` is a common shortcut, and a fair trade as long as you accept that anything semi-transparent comes out wrong.

Named colors occur, but the set the client accepts is not documented anywhere, and CCP's own data uses only two of them: `yellow` and `white`.

Do not pass a name straight to CSS. CSS knows `lightblue` and `lightgreen` too and will quietly paint its own values for them, which is the same silent-substitution trap as the byte order above. [RIFT's color table](https://gitlab.com/rift-intel-fusion-tool/rift-intel-fusion-tool/-/blob/release/src/main/kotlin/dev/nohus/rift/compose/text/ParseEveFormattedTextUseCase.kt) is the only published mapping and a reasonable starting point, but it is that project's reading rather than anything from the client — treat it as a guess you may need to correct.

!!! tip "Colors assume a dark background"
    Players and CCP alike pick colors that work on the client's near-black UI.
    On a light background, text written in `0xff000000` disappears and anything dark becomes unreadable.
    Render on a dark surface, or map the colors onto your own palette before rendering — and whichever you do, check the result against [WCAG's contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) rather than trusting the sender's taste.

## Links

The same link has two spellings:

```
<a href=showinfo:5//30000142>Jita</a>
<url=showinfo:5//30000142>Jita</url>
```

The value is a URI whose scheme names an in-game window and whose payload says what to show in it.
Ordinary `http:` and `https:` URLs appear too, and should be opened in a browser like any other link.

Which spelling you meet depends on where the text came from — the parsers that read mail bodies handle only `<a href="…">`, links copied out of chat arrive as `<url=…>`, and CCP's type descriptions contain both.
Handle either.

The link text is whatever the author typed.
It is not necessarily the entity's current name, so resolve the ID yourself with `/universe/names` if you want to display an authoritative one.

### Payload grammar

There is no single grammar, but the conventions are consistent:

- `//` separates a discriminator from an identifier, as in `showinfo:<typeID>//<itemID>`.
- `:` separates positional parts within a payload, as in `killReport:<killmailID>:<hash>`.
- Ignore segments you do not recognize rather than rejecting the link.

Scheme names are **camelCase** — `warReport`, `killReport`, `joinChannel`, `helpPointer`, `recruitmentAd`, `shipSkinListing`, `careerProgramNode`, `bookmarkFolder`.
This violates the lowercase convention of [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986) and breaks libraries that assume it.
Compare scheme names case-insensitively, and do not lowercase the content itself.

### Schemes

| Scheme and example | Opens |
| ------------------ | ----- |
| `showinfo:5//30000142` | Show Info, for a type or a specific entity — see [below](#showinfo) |
| `fitting:<dna>` | A fitting. The payload is a [Ship DNA](fitting.md#dna) string |
| `killReport:13807613:1d88cad6…` | A killmail, by ID and hash |
| `warReport:1234567` | A war report |
| `contract:0//196428637` | A contract. The contract ID is the *second* segment; the first is the solar system it is in, or `0` |
| `recruitmentAd:98645206//155600` | A corporation's recruitment ad. The corporation ID is the *first* segment |
| `joinChannel:-26572540` | Joins a chat channel. Player-created channel IDs are negative |
| `bookmarkFolder:7102471` | A shared bookmark folder |
| `fleet:1021212278338` | A fleet |
| `shipSkinListing:fe7ec0c3-2d02-…` | A SKIN listing. The payload is a UUID, not a numeric ID |
| `opportunity:epic_arcs:40` | Something the player can take on. The first part names the kind — `epic_arcs`, `corporation_goals`, `freelance_projects`, `mercenary_tactical_ops` — and the second is its ID |
| `careerProgramNode:7:410:None` | A node of the AIR Career Program |
| `helpPointer:neocom.airCareerProgram` | Points the player at a piece of the UI |
| `localsvc:method=OpenFWWindow` | Calls a named client-side service, usually to open a window |
| `openCareerAgents:` | The career agents window. The payload is empty |
| `evebrowser:http://…` | The in-game browser, gone since 2016. Only in old data |

Where this list comes from matters, because none of it is specified.
`showinfo:`, `fitting:`, `evebrowser:` and `openCareerAgents:` are the four that appear in CCP's own data, so their spelling and shape are certain.
The rest is drawn from what third-party parsers handle and from their test fixtures — chiefly [RIFT](../community/rift-intel-fusion-tool/index.md), [JitaSpace](../community/jitaspace/index.md) and [PodMail](https://github.com/zKillboard/podmail) — so read those payload grammars as observed rather than documented, and expect the segments nobody has explained yet to hold surprises.

Two more have been reported but are not confirmed even that far: `hyperNet:` for a HyperNet Relay offer with a UUID payload, and `shipSkinDesign:` alongside `shipSkinListing:`.

Treat an unfamiliar scheme the way you would treat an unfamiliar tag — render the link text, and either ignore the target or pass it through untouched.

### `showinfo`

By far the most common scheme, and the only one that takes real work to resolve.
It accounts for 3,311 of the 3,414 links in the SDE's English type descriptions.

```
showinfo:<typeID>
showinfo:<typeID>//<itemID>
```

With one segment it means "show this type" — the Show Info window for an inventory type, as if you had right-clicked the item on the market.

With two segments it means "show this specific thing", and **the typeID only tells you what kind of thing the itemID is**.
There is no field saying "this is a character": you are expected to know that `1377` is a character type, so `showinfo:1377//1795255388` is a character.

The pair makes sense once you know that everything the client can show info on — a character, a station, a moon, a region — is a row with both an `itemID` and a `typeID`, and the type is what decides which Show Info window to draw.

That is why so many third-party parsers carry hardcoded lists of station and character type IDs.
You do not have to.
Look the type up in the SDE, take its group and category, and decide from those:

| Condition on the typeID | The itemID is | Example |
| ----------------------- | ------------- | ------- |
| Group 1 (Character) | A character | `showinfo:1377//1795255388` |
| Group 2 (Corporation) | A corporation | `showinfo:2//1000125` |
| Group 19 (Faction) | A faction | `showinfo:30//500003` |
| Group 32 (Alliance) | An alliance | `showinfo:16159//632866070` |
| Group 3 (Region) | A region | `showinfo:3//10000041` |
| Group 4 (Constellation) | A constellation | `showinfo:4//20000603` |
| Group 5 (Solar System) | A solar system | `showinfo:5//30003413` |
| Category 2 (Celestial), any other group | A celestial: a planet, moon, stargate, beacon, wreck… | `showinfo:30889//40318018` (a planet), `showinfo:14//40245270` (a moon) |
| Category 3 (Station) | An NPC station | `showinfo:21646//61000002` |
| Category 65 (Structure) | A player-owned structure | `showinfo:35833//1021628175407` |
| Anything else | An individual item of that type | `showinfo:17926//2038831928` (a specific Cruor) |

Every example above except the last two is a link taken verbatim from a type description in the SDE.

--8<-- "snippets/eve-html/showinfo.md"

There is no canonical web equivalent for an in-game link — you choose one, and the kind above is the key.
Owners (`character`, `corporation`, `alliance`, `faction`) map to a profile page, `region`, `constellation` and `solar_system` to a map, `type` to an item database, `station` and `structure` to a location page.
For `item` there is nothing useful to link to: render the text and drop the target.

Groups 1, 2, 19 and 32 are the whole of category 1 (Owner), so a single category check covers all four if you do not care which kind of owner it is.
Without the SDE the same walk is two calls — `/universe/types/{type_id}` gives you `group_id` and `/universe/groups/{group_id}` gives you `category_id`.
For characters, corporations, alliances, stations and the map, `/universe/names` is a shortcut: pass it the itemID and it returns a `category` directly. It does not cover celestials, player structures or individual items, so it is not a full substitute — and since the IDs come out of a message a stranger wrote, expect some of them not to resolve. ESI leaves those out of the response rather than failing, and returns 404 only when none of them resolve.
Group 1 currently holds fifteen type IDs — 1373 to 1386 and 34574 — and which one a given character link carries varies, so treat all fifteen alike.

!!! tip "Resolve, don't hardcode"
    Copies of these ID lists circulate between projects and go stale.
    One widely copied "station types" list includes type ID 14, which is a Moon; none of them include the `Ancient Jovian Outpost` station type.
    A group and category lookup keeps working when CCP adds a structure type.

## Parsing

Parse in two passes: a tolerant tokenizer, then a lenient tree builder.
Both must be total — for any input they produce *something*, because there is no such thing as invalid EVE HTML.

### 1. Tokenize

Walk the string and emit three kinds of token: literal text, an opening tag with its attributes, and a closing tag.

--8<-- "snippets/eve-html/tokenizer.md"

### 2. Re-nest

Turn the flat token list into a tree.
The client never builds one — it applies and unapplies styles as it walks the stream, which is why open and close tags in real data cross each other so freely.

First, keep `<br>`, `<t>`, `<left>`, `<right>` and `<center>` out of it: they are markers rather than containers and never close, so the unclosed-tag rule below must not apply to them.
Nest a document inside its own line breaks and a forty-line mail comes out forty levels deep.

For everything else, one rule covers the whole table: for each opening tag, scan forward for a closing tag of the same name, counting nested opens of that name as you go; the tokens in between become its children, and parsing continues after the close.
Run off the end without finding one and the tag owns the rest of the document; meet a closing tag with nothing open and drop it.

That gives you this behavior:

| Input | Sensible behavior |
| ----- | ------------------ |
| `<b>bold` (never closed) | Apply the formatting to the rest of the document |
| `</b>` with nothing open | Ignore it |
| `<b>a<i>b</b>c</i>` (crossed) | Let the outer tag win; close the inner one with it |
| `<b>a<b>b</b>c</b>` (same tag nested) | Count depth so the tags pair correctly |
| `<blink>text</blink>` (unknown tag) | Drop the tag, keep `text` |

Crossed tags are not hypothetical.
Here is part of a corporation description straight out of ESI, with a `<b>` opened inside one `<font>` and closed inside the next:

```
<font size="14" color="#ff007fff"><b>More Information<br><br></font><font size="12" color="#ffd98d00"><a href="showinfo:1377//93337205">Ikarus Cesaille</a></b></font>
```

The client's rich-text editor also emits a lot of noise: empty `<font></font>` pairs, a fresh `<font>` around every run rather than nesting them, and formatting restated after every `<br>`.

### 3. Render

Map the tree onto whatever your UI uses.
If your renderer is HTML, build the elements from the tree rather than reassembling a string, and sanitize whatever you do produce.

**Turn off whitespace collapsing** — `white-space: pre-wrap` on the container — or the significant runs of spaces and the literal `\n` and `\r\n` breaks are lost. With `pre-wrap` the source newlines already break lines, so render `<br>` as a newline *or* as `<br>`, not both, or every line break doubles.

| Tag | Render as |
| --- | --------- |
| `<b>`, `<i>`, `<u>` | `<strong>`, `<em>`, `<u>` |
| `<uppercase>` | `text-transform: uppercase` |
| `<font size=…>`, `<fontsize=…>` | `font-size`, scaled — see [Font size](#font-size) |
| `<font color=…>`, `<color=…>` | `color`, after splitting off the alpha |
| `<letterspace=…>` | `letter-spacing` |
| `<hint=…>`, and a link's `alt` | `title` |
| `<a>`, `<url=…>` | `<a>`, after rewriting the target |
| `<br>` | A line break |
| `<left>`, `<right>`, `<center>` | `text-align` on the current line |
| `<t>` | A column break within the line |
| `<loc>`, and anything unrecognized | Nothing — keep the contents |

## Rendering safely

Every byte of a mail body was written by another player, and any player can mail you.
Treat it as hostile input.

- **Never put the raw string into `innerHTML`.**
- **Rewrite EVE URI schemes before sanitizing, not after.** Sanitizers allow a fixed set of schemes by default, so `showinfo:` links are dropped as unknown protocols — the `<a>` and its text survive and only the target vanishes, which reads as a styling bug rather than a security control doing its job. Rewrite the schemes into your own URLs first, or add them to the sanitizer's allow-list. In DOMPurify that is `ALLOWED_URI_REGEXP`, which *replaces* the default pattern rather than adding to it — start from DOMPurify's own pattern and add the EVE scheme names to the alternation, or you will strip the `href` off every ordinary web link in the mail. Never widen it to everything: that puts `javascript:` back.
- **Watch the tag names your sanitizer does not know.** DOMPurify's HTML profile keeps `b`, `i`, `u`, `a`, `br` and `font` with their `size` and `color` attributes — but every tag unique to this format is an unknown element to it and is dropped: `<url=…>`, `<color=…>`, `<fontsize=…>`, `<hint=…>`, `<localized>`, `<loc>`. `<url=…>` is the one that will hurt, since it is the only link spelling in text copied out of chat. Convert those to tags your sanitizer knows before you hand it the string.
- **Strip `style`.** EVE's `<font>` accepts any attribute at all, so `<font style="position:fixed;inset:0">` is valid markup that the game ignores and your page honors — an attacker-supplied overlay across your whole UI. DOMPurify's HTML profile passes it through untouched, and nothing in this format needs it.
- **Validate a color before putting it in CSS.** If you paste EVE's `color` value into a CSS declaration unchecked, a crafted value can close the declaration and add its own. Match it against the three forms above and reject anything else.
- **Remember that link text is attacker-controlled.** Nothing ties the words in a link to the entity it points at, so a mail can label a `showinfo:` link with somebody else's name. If it matters to your users, resolve the ID and show the real one.

### Opening links in the client

If your application runs alongside the game, you can act on a link in-game instead of in your own UI:

- `/ui/openwindow/information` opens Show Info for a character, corporation or alliance.
- `/ui/openwindow/marketdetails` opens the Market Details window for a type.
- `/ui/openwindow/contract` opens a contract — the second segment of a `contract:` link.
- `/ui/autopilot/waypoint` is usually the more useful thing to do with a solar system or station link than opening Show Info on it.
- `/ui/openwindow/newmail` opens the mail composer with a body you supply. Since that body is EVE HTML it can contain any link at all, which makes it a general-purpose way to hand the player something clickable that no endpoint covers — [RIFT](../community/rift-intel-fusion-tool/index.md) uses it exactly this way. `subject`, `body` and at least one recipient are all required, so address the draft to the player themselves when you are only using it to carry a link.

These need the `esi-ui.open_window.v1` scope and a character who is logged in.

## Writing EVE HTML

Mail bodies you send with `/characters/{character_id}/mail` (scope `esi-mail.send_mail.v1`) may contain the same markup.

- **Markup counts against the length limit.** ESI accepts a body of up to 10,000 characters and a subject of up to 1,000, and every tag counts — a single color change costs about 30 characters.
- **Escape `&`, `<` and `>` in text you did not author, in that order.** `&` first — doing it last double-escapes what you just wrote, and skipping it means any `&amp;` or `&nbsp;` already in the text is decoded by the recipient's client and the text changes under them. A bare `<` is read as the start of a tag, and if nothing later in the body has a `>`, everything after it is thrown away.

Build links with the `<url=…>` form and the schemes above:

```
<url=showinfo:5//30000142>Jita</url>
<url=showinfo:648>Badger</url>
<url=showinfo:2//1000125>CONCORD</url>
```

For a `fitting:` link, the payload is a [Ship DNA](fitting.md#dna) string.

## What we still don't know

The gaps are worth stating plainly, because guessing at them is how a wrong answer spreads:

- **The full list of URI schemes.** Schemes are payloads the UI hands to other code rather than something the parser knows, so there is no list to read off — only what people have run into.
- **What some payload segments mean.** The second segment of `recruitmentAd:`, and all three parts of `careerProgramNode:`.
- **Which named colors the client accepts, and what values it gives them.** Only `yellow` and `white` can be evidenced from CCP's data.
- **What `<font size>` is relative to.** The engine measures in pixels, but the client scales on top of that and publishes no default.
- **What consumes `<loc>`,** and whether it takes attributes.

If you can settle any of these — ideally with a captured example — please open a pull request.
