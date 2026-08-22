import re
from dataclasses import dataclass, field

# A tag looks like `<name>`, `</name>`, `<name/>`, `<name key="value" ...>` or
# `<name=value>`. Everything else that starts with `<` is literal text.
# The tag ends at the first `>`. That is not quite the client's rule — it lets a
# quoted value contain a `>` — but making the pattern quote-aware costs more
# than it gains, because unbalanced quotes are common in player-written text.
TAG = re.compile(
    r"""<
        (?P<closing>/?)
        (?P<name>[A-Za-z][A-Za-z0-9]*)
        (?P<body>[^>]*)
        >""",
    re.VERBOSE,
)

# An attribute name, preceded by any amount of separating whitespace. `&nbsp;`
# separates attributes just as a space does.
ATTRIBUTE = re.compile(r"(?:\s|&nbsp;)*(?P<key>[A-Za-z][A-Za-z0-9]*)\s*=", re.IGNORECASE)

# A value is either quoted, or bare and terminated by a space, a tab, a `>` or
# an `&nbsp;` — so a bare value cannot contain a space.
VALUE = re.compile(
    r"""(?:"(?P<double>[^"]*)"
        |'(?P<single>[^']*)'
        |(?P<bare>(?:(?!&nbsp;)[^ \t>])*))""",
    re.VERBOSE | re.IGNORECASE,
)

# Tags that never have a closing tag. A trailing `/` is not a usable signal:
# CCP's own data writes 73,000 line breaks as `<br>` and none as `<br/>`.
VOID = {"br", "t", "left", "right", "center"}

# The only four character entities the client decodes. Note that `&nbsp;`
# becomes an ordinary space, and that anything else starting with `&` —
# including `&quot;` and numeric entities such as `&#39;` — is literal text.
ENTITIES = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&nbsp;": " "}
ENTITY = re.compile("|".join(ENTITIES), re.IGNORECASE)


def unescape(text: str) -> str:
    return ENTITY.sub(lambda m: ENTITIES[m.group(0).lower()], text)


@dataclass
class Text:
    text: str


@dataclass
class OpenTag:
    name: str                                       # lowercased; tags are case-insensitive
    attributes: dict[str, str] = field(default_factory=dict)
    void: bool = False                              # never closed, so never a container


@dataclass
class CloseTag:
    name: str


def value_of(match: re.Match) -> str:
    for group in ("double", "single", "bare"):
        if match[group] is not None:
            return match[group]
    return ""


def parse_attributes(name: str, body: str) -> dict[str, str]:
    attributes: dict[str, str] = {}
    position = 0

    # `<url=showinfo:5//30000142>` carries a value rather than named attributes.
    # Store it under the tag's own name, so that `<url=x>` and `<a href="x">`
    # can be handled the same way afterwards. The legacy `<url:x>` spelling
    # means the same thing — the client rewrites the `:` to an `=` first.
    if body[:1] == "=" or (name == "url" and body[:1] == ":"):
        match = VALUE.match(body, 1)
        attributes[name] = value_of(match)
        position = match.end()

    # Named attributes follow, including after a tag value: the client emits
    # `<url=showinfo:5//30000142 alt='Current Solar System'>`. Keys are
    # lower-cased here for convenient lookup, but note that the client keeps
    # whatever case they were written in.
    while (attribute := ATTRIBUTE.match(body, position)) is not None:
        match = VALUE.match(body, attribute.end())
        attributes[attribute["key"].lower()] = value_of(match)
        position = match.end()

    return attributes


def tokenize(markup: str) -> list[Text | OpenTag | CloseTag]:
    tokens: list[Text | OpenTag | CloseTag] = []
    position = 0

    while position < len(markup):
        match = TAG.search(markup, position)
        if match is None:
            tokens.append(Text(unescape(markup[position:])))
            break

        # Anything before the tag is literal text, including any `<` that did
        # not start a tag. The client is less forgiving here: it treats every
        # `<` as the start of a tag and discards up to the next `>`.
        if match.start() > position:
            tokens.append(Text(unescape(markup[position:match.start()])))

        name = match["name"].lower()
        # The client requires an attribute-less tag to be written exactly, and
        # reads `<b >` as an unknown tag. Accepting the stray space here is a
        # second deliberate divergence.
        body = match["body"].strip()
        if match["closing"]:
            tokens.append(CloseTag(name))
        else:
            tokens.append(OpenTag(name, parse_attributes(name, body), name in VOID))

        position = match.end()

    return tokens
