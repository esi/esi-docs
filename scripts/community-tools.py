import os
import posixpath

from mkdocs.exceptions import PluginError
from mkdocs.plugins import get_plugin_logger
from mkdocs.utils import get_relative_url
from mkdocs.utils.meta import get_data

log = get_plugin_logger(__name__)

meta = {}
env = None
macros = None

# A community page must declare exactly one of these as its kind. The value is
# compared case-sensitively when building the tables, so casing matters.
ALLOWED_TYPES = ("service", "resource")

# A maintainer can be linked in one of these ways; at least one is required.
MAINTAINER_SOURCES = ("github", "gitlab", "repository")

# Community pages that intentionally don't follow the service/resource contract
# and must therefore be skipped by the validator.
SKIP_VALIDATION = frozenset(
    {
        "community/index.md",  # the listing page itself
        "community/sample-service/index.md",  # the template
    }
)


def on_files(files, *, config):
    global meta
    global env

    meta = {}
    env = config.theme.get_env()

    for file in files:
        name = posixpath.basename(file.src_uri)
        if name != "index.md":
            continue
        with open(file.abs_src_path, encoding="utf-8-sig") as fh:
            try:
                [_, data] = get_data(fh.read())
                meta[file] = data
            except Exception as e:
                raise PluginError(f"Error parsing {file.src_path}: {e}") from e

    _validate_community_meta()


def _validate_page(data):
    """Return a list of problems with a community page's front matter.

    An empty list means the page satisfies the contract that the community
    tables and ``overrides/community/simple.html`` rely on. Anything else would
    otherwise fail silently — e.g. a mis-cased ``type`` drops the page from the
    tables with no error at all.
    """
    problems = []

    kind = data.get("type")
    if kind not in ALLOWED_TYPES:
        problems.append(
            f"'type' is {kind!r} but must be exactly one of "
            f"{list(ALLOWED_TYPES)} (lowercase); otherwise the page is "
            "silently omitted from the community tables"
        )

    if not str(data.get("title") or "").strip():
        problems.append("'title' is required and must be non-empty")

    if not str(data.get("description") or "").strip():
        problems.append("'description' is required and must be non-empty")

    maintainer = data.get("maintainer")
    if not isinstance(maintainer, dict):
        problems.append(
            "'maintainer' is required and must be a mapping with a 'name' and "
            "at least one of " + ", ".join(MAINTAINER_SOURCES)
        )
    else:
        if not str(maintainer.get("name") or "").strip():
            problems.append("'maintainer.name' is required and must be non-empty")
        if not any(str(maintainer.get(k) or "").strip() for k in MAINTAINER_SOURCES):
            problems.append(
                "'maintainer' must define at least one of "
                + ", ".join(MAINTAINER_SOURCES)
            )

    return problems


def _validate_community_meta():
    """Warn about malformed community pages.

    Problems are logged as warnings so local ``mkdocs serve`` still renders,
    while CI (``make test`` runs ``mkdocs build --strict``) promotes them to
    build failures — catching bad metadata before it silently breaks the tables.
    """
    for file, data in meta.items():
        src = file.src_uri
        if not src.startswith("community/") or src in SKIP_VALIDATION:
            continue
        for problem in _validate_page(data):
            log.warning("%s: %s", src, problem)


def community_pages(filter="service"):
    tpl = env.select_template(
        [
            f"community/{filter}.html",
            f"community/{filter}.md",
        ]
    )

    file = macros.page.file
    dname = os.path.dirname(file.src_path)
    files = [f for f in meta if f.src_path.startswith(f"{dname}/") and f != file]
    items = sorted(
        [
            (
                meta[f].get("title", os.path.basename(os.path.dirname(f.src_path))),
                f,
                meta[f],
            )
            for f in files
            if meta[f].get("type") == filter
        ],
        key=lambda it: str(it[0]).casefold(),
    )
    return tpl.render(
        items=items,
        filter=filter,
        config=macros.config,
        page=macros.page,
        base_url=get_relative_url(".", macros.page.url),
    )


FUNCTIONS = {"community_pages": community_pages}


def on_config(config, **kwargs):
    global macros
    macros = config.plugins.get("macros")
    macros.register_macros(FUNCTIONS)
