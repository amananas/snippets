"""
This snippets aims to configure the logging utility, to get richer behavior.
The logging utility will then be used for both user output, and file logging, depending ont the level used.
"""

import logging
import logging.config

##########################################
# Define submodules to shut down, to avoid excessive output.
##########################################
_SUBMODULES_CHANGED_LEVELS = {
    'example': logging.ERROR
}

##########################################
# Defining a valid level and callbacks in the logging utility, for greenish output
##########################################

logging.VALID = 25
logging.valid = lambda msg, *args, **kwargs: logging.log(logging.VALID, msg, *args, **kwargs)
logging.Logger.valid = lambda self, msg, *args, **kwargs: self.log(logging.VALID, msg, *args, **kwargs)
logging.addLevelName(logging.VALID, "VALIDATION")

##########################################
# Part to configure to get the expected output
##########################################
_COLOR_CODES = {
    'critical': '\033[31m\033[1m',
    'error': '\033[31m',
    'warning': '\033[33m',
    'valid': '\033[32m',
    'none': '\033[0m'
}
_LOGS_FILENAME = None


##########################################
# Filter class, as used by the logging utility
##########################################
class _Filter:

    def __init__(self, level):
        self._level = level

    def getLevel(self):
        """ Return this filter level, accoring to the logging utility. """
        return self._level

    def filter(self, log):
        """ Filtering for the logging utility. Filter out whatever is higher than this filter level. """
        return log.levelno <= self._level


##########################################
# Main part
##########################################
_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'critical': {
            'format': _COLOR_CODES['critical'] + '%(message)s' + _COLOR_CODES['none']
        },
        'error': {
            'format': _COLOR_CODES['error'] + '%(message)s' + _COLOR_CODES['none']
        },
        'warning': {
            'format': _COLOR_CODES['warning'] + '%(message)s' + _COLOR_CODES['none']
        },
        'valid': {
            'format': _COLOR_CODES['valid'] + '%(message)s' + _COLOR_CODES['none']
        },
        'info': {
            'format': _COLOR_CODES['none'] + '%(message)s' + _COLOR_CODES['none']
        },
        'debug': {
            'format': _COLOR_CODES['none'] + '%(message)s' + _COLOR_CODES['none']
        }
    },
    'filters': {
        'critical-only': {
            '()': _Filter,
            'level': logging.CRITICAL
        },
        'error-only': {
            '()': _Filter,
            'level': logging.ERROR
        },
        'warning-only': {
            '()': _Filter,
            'level': logging.WARNING
        },
        'valid-only': {
            '()': _Filter,
            'level': logging.VALID
        },
        'info-only': {
            '()': _Filter,
            'level': logging.INFO
        },
        'debug-only': {
            '()': _Filter,
            'level': logging.DEBUG
        }
    },
    'handlers': {
        'logsfile': {
            'level': 'DEBUG',
            'formatter': 'file',
            'class': 'logging.FileHandler',
            'mode': 'w'
        },
        'console-critical': {
            'level': 'CRITICAL',
            'formatter': 'critical',
            'filters': ['critical-only'],
            'class': 'logging.StreamHandler'
        },
        'console-error': {
            'level': 'ERROR',
            'formatter': 'error',
            'filters': ['error-only'],
            'class': 'logging.StreamHandler'
        },
        'console-warning': {
            'level': 'WARNING',
            'formatter': 'warning',
            'filters': ['warning-only'],
            'class': 'logging.StreamHandler'
        },
        'console-valid': {
            'level': logging.VALID,
            'formatter': 'valid',
            'filters': ['valid-only'],
            'class': 'logging.StreamHandler'
        },
        'console-info': {
            'level': 'INFO',
            'formatter': 'info',
            'filters': ['info-only'],
            'class': 'logging.StreamHandler'
        },
        'console-debug': {
            'level': 'DEBUG',
            'formatter': 'debug',
            'filters': ['debug-only'],
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'propagate': True
        }
    }
}


def configLogging(displayDebug=False):
    """
    Configure the logging utility, according to this very configuration file
    """

    if _LOGS_FILENAME:
        _LOGGING_CONFIG['handlers']['logsfile']['filename'] = _LOGS_FILENAME
    else:
        del _LOGGING_CONFIG['handlers']['logsfile']
    if not displayDebug:
        del _LOGGING_CONFIG['handlers']['console-debug']
    _LOGGING_CONFIG['loggers']['']['handlers'] = [key for key in _LOGGING_CONFIG['handlers']]
    logging.config.dictConfig(_LOGGING_CONFIG)

    if not displayDebug:
        for submodule, level in _SUBMODULES_CHANGED_LEVELS.items():
            logging.getLogger(submodule).setLevel(level)
