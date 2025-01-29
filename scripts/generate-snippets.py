#!/usr/bin/env python3

from os.path import join, dirname, abspath, splitext
from os import walk

#
# Configuration
#
# The mapping of file extensions to language names. The key is the file extension
# (including the dot), and the value is the language name.
# The name will be used in the generated markdown file.
EXTENSION_MAPPING = {
    ".py": "Python",
    ".cs": "C#",
    ".kt": "Kotlin",
}

# The mapping of file extensions to syntax highlighting names. The key is the file
# extension (including the dot), and the value is the syntax highlighting name.
SYNTAX_MAPPING = {
    ".py": "python",
    ".cs": "csharp",
    ".kt": "kotlin",
}

# The file extension for the combined markdown file.
COMBINED_EXT = ".md"

#
# End of configuration
#

# We sort the languages by their name to ensure a consistent order in the generated file.
LANGUAGE_ORDER = sorted(EXTENSION_MAPPING.items(), key=lambda x: x[1])

# The path to the snippets folder.
snipets_path = abspath(join(dirname(abspath(__file__)), "..", "snippets"))


# We could use pathlib/relpath, but this is simpler, and since we're not dealing
# with user input, it's safe enough.
def path_to_snippet(fname):
    if not fname.startswith(snipets_path):
        return None
    return f"snippets/{fname[len(snipets_path) + 1:]}"


def write_if_changed(fname, content):
    try:
        with open(fname, "r") as f:
            old_content = f.read()
    except FileNotFoundError:
        old_content = None

    if old_content != content:
        with open(fname, "w") as f:
            f.write(content)


# Process a folder and generate combined markdown files based on the snippets found.
def process_folder(path, files):
    found = {}
    for fname in files:
        base, ext = splitext(fname)
        if ext not in EXTENSION_MAPPING:
            continue
        found.setdefault(base, []).append(ext)
    for base, exts in found.items():
        fname = join(path, f"{base}{COMBINED_EXT}")
        content = []
        for ext, lang in LANGUAGE_ORDER:
            if ext in exts:
                infile = join(path, f"{base}{ext}")
                content.extend(
                    [
                        f'=== "{lang}"',
                        "",
                        f"    ```{SYNTAX_MAPPING[ext]}",
                        f'    --8<-- "{path_to_snippet(infile)}"',
                        f"    ```",
                    ]
                )
        content.append("")
        write_if_changed(fname, "\n".join(content))


def generate():
    for root, _, files in walk(snipets_path):
        process_folder(abspath(join(snipets_path, root)), files)


def on_pre_build(**kwargs):
    generate()
