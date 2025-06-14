from logging import getLogger

log = getLogger(__name__)

log.info("Hello World!")


def context(a, b):
    return a + b
