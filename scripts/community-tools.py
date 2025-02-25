import os
import posixpath
from mkdocs.exceptions import PluginError
from mkdocs.utils import get_relative_url
from mkdocs.utils.meta import get_data

meta = {}
env = None
macros = None


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
        ]
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
