import logging
from mkdocs_macros import util

# Make mkdocs-macros only output on verbose mode
util.TRACE_LEVELS["info"] = logging.DEBUG


def define_env(env):
    pass
