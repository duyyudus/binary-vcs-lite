import os
import sys
import functools
import time
import json
import re
import shutil
import copy
import logging
from pprint import pformat

if sys.version_info[0] == 3:
    from pathlib import Path, PurePath
else:
    from pathlib2 import Path, PurePath

from .config import *

# int: 0, 1, 2, 3, 4, 5
#   Set to 0 to turn off
_global_log_level = 0


class VcsLiteError(Exception):
    """Base error for version control operations."""

    def __init__(self, message='', vcs_logger=None):
        super(VcsLiteError, self).__init__()
        self._message = message
        if vcs_logger:
            vcs_logger.log_error(message)
        else:
            print('{}'.format(message))

    def __str__(self):
        return self._message


class PathMustBeAbsolute(VcsLiteError):
    """Path must be absolute."""

    def __init__(self, message='', vcs_logger=None):
        super(PathMustBeAbsolute, self).__init__(message, vcs_logger)


class InvalidType(VcsLiteError):
    """Invalid type."""

    def __init__(self, message='', vcs_logger=None):
        super(InvalidType, self).__init__(message, vcs_logger)


class InvalidPath(VcsLiteError):
    """Invalid path.

    Condition:
        Passing relative path to a must-be-absolute path parameter
        Path starts with POSIX root on windows system, and vice versa
    """

    def __init__(self, message='', vcs_logger=None):
        super(InvalidPath, self).__init__(message, vcs_logger)


class VcsLogger(object):
    """Custom logger for file versioning operations

    How to use:
        Create an instance of this class in global scope of target module
        Setup that instance using info of target module
        Pass that instance to any function/method that need to log
    """

    def __init__(self):
        super(VcsLogger, self).__init__()
        self.lvl_map = {
            1: logging.DEBUG,
            2: logging.INFO,
            3: logging.WARNING,
            4: logging.ERROR,
            5: logging.CRITICAL,
        }
        self.lvl = self.lvl_map[_global_log_level] if _global_log_level else logging.INFO
        self.log_name = LOG_PREFIX

        # Default root logger
        self.logger = logging.getLogger()
        if self.logger.handlers:
            self.logger.handlers = []
        self.logger.setLevel(self.lvl)
        ch = logging.StreamHandler()
        ch.setLevel(self.lvl)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def setup(self, log_file, log_name, log_level=2, save_log_file=0):
        self.log_file = log_file
        self.log_name = log_name
        self.lvl = self.lvl_map[_global_log_level] if _global_log_level else self.lvl_map[log_level]

        # Remove root logger handlers first
        root_logger = logging.getLogger()
        if root_logger.handlers:
            root_logger.handlers = []

        # New logger
        self.logger = logging.getLogger(log_name)
        if self.logger.handlers:
            self.logger.handlers = []

        self.logger.setLevel(self.lvl)

        # Create file handler and set level
        if save_log_file:
            if not Path(log_file).parent.exists():
                Path(log_file).parent.mkdir(parents=1)
            fh = logging.FileHandler(filename=str(log_file), mode='a')
            fh.setLevel(self.lvl)

        # Create console handler and set level
        ch = logging.StreamHandler()
        ch.setLevel(self.lvl)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s')

        # Add formatter
        if save_log_file:
            fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add handlers to self.logger
        self.logger.addHandler(ch)
        if save_log_file:
            self.logger.addHandler(fh)

    def _log_message(self, args):
        def fstr(s):
            if type(s) is str:
                return s
            else:
                return '\n' + pformat(s)

        _log_indent = 0
        message = ''.join([fstr(a) for a in args])
        return (''.join([' ' for i in range(_log_indent * 4)]), message)

    def set_log_level(self, log_level):
        """
        Args:
            lvl (int): log level
                0: logging.DEBUG
                1: logging.INFO
                2: logging.WARNING
                3: logging.ERROR
                4: logging.CRITICAL
        """
        self.lvl = self.lvl_map[log_level]
        self.logger.setLevel(self.lvl)

        for h in self.logger.handlers:
            h.setLevel(self.lvl)
            for f in h.formatters:
                f.setLevel(self.lvl)

    def log_debug(self, *args):
        indent_str, message = self._log_message(args)
        if not message:
            print('')
            return 0

        self.logger.debug('{} :: {}'.format(
            self.log_name,
            indent_str + message
        ))

    def log_info(self, *args):
        indent_str, message = self._log_message(args)
        if not message:
            print('')
            return 0

        self.logger.info('{} :: {}'.format(
            self.log_name,
            indent_str + message
        ))

    def log_error(self, *args):
        indent_str, message = self._log_message(args)
        if not message:
            print('')
            return 0

        self.logger.error('{} :: {}'.format(
            self.log_name,
            indent_str + message
        ))


def _time_measure(func):
    """Measure running time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        print('Running time of {}() : {} seconds'.format(func.__name__, str(time.time() - st)))
        return ret
    return wrapper


def set_global_log_level(log_level):
    global _global_log_level
    _global_log_level = log_level


def match_regex_pattern(input_str, patterns):
    """
    Args:
        input_str (str):
        patterns (list of str):
    Returns:
        bool:
    """
    check_type(input_str, [str])
    check_type(patterns, [list])

    for p in patterns:
        if re.findall(p, input_str):
            return 1


def copy_file(source, target, vcs_logger, overwrite=0):
    """Copy file and return result code.

    `source` and `target` will be converted to `str`.

    Args:
        source (str|Path):
        target (str|Path):
    Returns:
        ternary:
            -1: skipped
            0: failed
            1: succeed
    """

    source = str(source)
    target = str(target)

    if not Path(target).parent.exists():
        try:
            Path(target).parent.mkdir(parents=1)
        except Exception as e:
            vcs_logger.log_error('Copy mkdir error: {}'.format(target))
            vcs_logger.log_error('----{}'.format(str(e)))
            return 0

    if overwrite and Path(target).exists():
        try:
            os.remove(target)
        except Exception as e:
            vcs_logger.log_error('Copy overwrite error: {}'.format(target))
            vcs_logger.log_error('----{}'.format(str(e)))
            return 0

    if Path(target).exists():
        return -1
    else:
        try:
            shutil.copyfile(source, target)
        except Exception as e:
            if Path(target).exists():
                try:
                    os.remove(target)
                except Exception:
                    pass
            vcs_logger.log_error('Copy error: {}'.format(target))
            vcs_logger.log_error('----{}'.format(str(e)))
            return 0
        vcs_logger.log_debug('Copied: {}'.format(target))
        return 1


def batch_copy(path_pair, vcs_logger, message='Copied file', overwrite=0):
    """
    Args:
        path_pair (list of 2-tuple): List of 2-tuple of str, [(source, target),...]
    Returns:
        list of str: List of copied file paths
    """

    copied = []
    batch_size = len(path_pair)
    for i, p in enumerate(path_pair):
        source, target = p
        if copy_file(source, target, vcs_logger, overwrite) == 1:
            copied.append(str(target))
        vcs_logger.log_info('{}: {}/{}'.format(message, str(i + 1), batch_size))

    vcs_logger.log_info('Total newly copied files: {}'.format(len(copied)))
    return copied


def load_json(json_path, vcs_logger):
    """
    Args:
        json_path (str|Path):
    Returns:
        dict:
    """

    json_path = str(json_path)

    if not Path(json_path).exists():
        vcs_logger.log_debug('JSON not found: {}'.format(json_path))
        return {}

    with open(str(json_path), 'r') as f:
        vcs_logger.log_debug('Loaded JSON: {}'.format(json_path))
        return json.loads(f.read())


def save_json(data, json_path, vcs_logger):
    """
    Args:
        json_path (str|Path):

    """

    json_path = Path(json_path)

    if not json_path.parent.exists():
        json_path.parent.mkdir(parents=1)

    with open(str(json_path), 'w') as f:
        f.write(json.dumps(data, indent=2))
        vcs_logger.log_debug('Saved JSON: {}'.format(str(json_path)))


def check_path(input_path):
    """
    Args:
        input_path (str|Path):
    Raises:
        PathMustBeAbsolute:
        InvalidPath:
    Returns:
        bool:
    """
    input_path = Path(input_path)
    if os.name == 'nt':
        if input_path.as_posix()[:2] != '//' and input_path.as_posix().startswith('/'):
            raise InvalidPath('InvalidPath: {}'.format(input_path.as_posix()))
    elif not (input_path.is_absolute() or input_path.as_posix().startswith('/')):
        raise PathMustBeAbsolute('PathMustBeAbsolute: {}'.format(input_path.as_posix()))
    return 1


def check_type(obj, types, raise_exception=1):
    """Assert type of `obj`

    Args:
        obj:
        types (list): list of types/classes
    Raises:
        InvalidType:
    Returns:
        bool:
    """

    if str in types and sys.version_info[0] == 2:
        types.append(unicode)

    if isinstance(obj, tuple(types)):
        return 1
    elif raise_exception:
        msg = '"{}" ({}) must be an instance of ({})'.format(
            str(obj),
            type(obj),
            ', '.join([str(t) for t in types])
        )
        raise InvalidType(msg)
    else:
        return 0


def make_hidden(input_path, vcs_logger):
    """Make file/folder hidden ( window only so far )

    Args:
        input_path (str|Path):
    """
    check_type(input_path, [str, Path])

    input_path = str(input_path)
    try:
        os.system('attrib +h {}'.format(input_path))
    except Exception as e:
        vcs_logger.log_error('Cannot make hidden: {}'.format(input_path))
        vcs_logger.log_error('----'.format(str(e)))
