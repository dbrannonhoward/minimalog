from collections.abc import Iterable
from inspect import FrameInfo
from os.path import exists as path_exists
from pathlib import Path
import inspect
import logging
import os

ERROR_LEVELS = (logging.INFO, logging.DEBUG, logging.WARNING, logging.ERROR)


class MinimalLog:
    def __init__(self, logger_name=None):
        """:param logger_name: if is None, return root logger, else return logger for module __name__"""
        self.log_extension = get_log_extension()
        self.log_format, self.time_format = get_format_strings()  # time_format not used
        try:
            self.logger = logging.getLogger() if logger_name is None else logging.getLogger(__name__)
        except Exception as e_err:
            print(f'error with logging.getLogger()')
            for arg in e_err.args:
                print(arg)
        msg = f'initializing \'{self.__class__.__name__}\''
        self.INFO, self.DEBUG, self.WARNING, self.ERROR = ERROR_LEVELS
        try:
            self._configure_(verbosely=True)  # cannot log before this call
            self.log(msg, announcement=True, event_completed=False)
            self.log(msg, announcement=True, event_completed=True)
            # value = potato
        except Exception as e_err:
            self.log(e_err)

    @staticmethod
    def clean_up():
        delete_list_of_files(find_log_files())

    def debug(self, msg='') -> None:
        try:
            self.logger.debug(msg=msg)
        except Exception as e_err:
            for arg in e_err.args:
                print(arg)

    def info(self, msg) -> None:
        try:
            self.logger.info(msg=msg)
        except Exception as e_err:
            for arg in e_err.args:
                print(arg)

    def log(self, msg, event_completed=None, level=logging.INFO, announcement=False,
            dump_call_stack=False, call_deprecated=True) -> None:
        # FIXME delete me before merge
        # FIXME delete me before merge
        call_deprecated = False
        # FIXME delete me before merge
        # FIXME delete me before merge
        if call_deprecated:
            _log_deprecated(self, msg, event_completed, level, announcement, dump_call_stack)
            return
        try:
            if isinstance(msg, Exception):
                self._log_exception(msg)
                return
            _log_deprecated(self, msg, event_completed, level, announcement, dump_call_stack)
        except Exception as e_err:
            for arg in e_err.args:
                print(arg)

    def set_level(self):
        msg = f'setting level for logger'
        try:
            self.log(msg)
        except Exception as e_err:
            self.log(e_err)

    def _configure_(self, verbosely=False):
        filemode = get_log_filemode()
        try:
            logging.basicConfig(filename=get_log_filename(), filemode=filemode,
                                level=get_default_level(), format=self.log_format)
            if verbosely:
                self.debug(f'logger propagation set to \'{self.logger.propagate}\'')
                self.debug(f'logger effective level is \'{self.logger.getEffectiveLevel()}\'')
        except Exception as e_err:
            for arg in e_err.args:
                print(arg)

    def _log_exception(self, exc) -> None:
        try:
            exc_type = type(exc)
            for arg in exc.args:
                self.log(f'{exc_type} : {arg}')
        except Exception as e_err:
            for arg in e_err.args:
                print(arg)


def delete_list_of_files(files_to_delete: list):
    try:
        for file in files_to_delete:
            if path_exists(file):
                os.remove(file)
    except Exception as e_err:
        for arg in e_err.args:
            print(arg)


def find_log_files() -> list:
    log_files = list()
    try:
        for root, directories, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith('log'):
                    log_files.append(Path(root, file))
        return log_files
    except Exception as e_err:
        for arg in e_err.args:
            print(arg)


def get_call_stack_above_logger(function_names_in_call_stack: list) -> list:
    try:
        call_stack_container = list()
        # create a list of appropriate size to store the call stack
        # sets 'blank_spaces' count of unused spaces in list as visual delimiter
        blank_spaces = 1
        call_stack_container_size = len(function_names_in_call_stack) + blank_spaces
        # pre-populate list to larger than needed, and allowing negative indices
        for container_section in range(call_stack_container_size):
            call_stack_container.append('x')
        # write the call stack to the list, burying less-relevant calls in negative indices
        for num, stack_frame_name in enumerate(function_names_in_call_stack):
            call_stack_container[num-2] = stack_frame_name
        call_stack_above_logger = list()
        for num, call_frame_function_name in enumerate(call_stack_container):
            if not num:
                continue
            if call_frame_function_name == 'x':
                break
            call_stack_above_logger.append(call_frame_function_name)
        return call_stack_above_logger
    except Exception as e_err:
        for arg in e_err.args:
            print(arg)


def get_caller_from_(frame: FrameInfo) -> str:
    try:
        caller_name = ''
        frame_at_function_name_index = frame[3]
        if frame_at_function_name_index is not None:
            caller_name = frame_at_function_name_index
        return caller_name
    except Exception as e_err:
        for arg in e_err.args:
            print(arg)


def get_default_level() -> int:
    return logging.INFO


def get_format_string_for_msg():
    # reference : https://docs.python.org/3/library/logging.html#logrecord-attributes
    return "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : %(message)s"


def get_format_string_for_time():
    # reference : https://docs.python.org/3/library/time.html#time.strftime
    return "%Y-%m-%d, %H:%M:%S"


def get_format_strings():
    return get_format_string_for_msg(), get_format_string_for_time()


def get_function_names_in_call_stack() -> list:
    stack = get_stack(filter_system_frames=True)
    function_names_in_call_stack = list()
    for frame in stack:
        caller = get_caller_from_(frame)
        function_names_in_call_stack.append(caller)
    return function_names_in_call_stack


def get_log_extension() -> str:
    return "log"


def get_log_filemode(append=True) -> str:
    return 'a' if append else 'w'


def get_log_filename() -> str:
    return "event.log"


def get_stack(filter_system_frames=True) -> inspect.stack:
    try:
        stack = inspect.stack()
        if filter_system_frames:
            stack = remove_system_frames_from_(stack)
        return stack
    except Exception as e_err:
        for arg in e_err.args:
            print(arg)


def get_stack_depth(stack) -> int:
    stack_depth_count = 0
    try:
        for _ in stack:
            stack_depth_count += 1
    except Exception as e_err:
        for arg in e_err.args:
            print(arg)
    return stack_depth_count


def not_system_(caller_name: str) -> bool:
    stack_calls_to_filter = ['_call_with_frames_removed', '_exec', 'exec_module', 'execfile',
                             '_find_and_load', '_find_and_load_unlocked', '_load_unlocked']
    try:
        if caller_name is None:  # filter None
            return False
        if caller_name in stack_calls_to_filter:
            return False
        if caller_name.endswith('__') or caller_name.endswith('>'):
            return False  # filter dunder, <module>,
        return True
    except Exception as e_err:
        for arg in e_err.args:
            print(arg)


def remove_system_frames_from_(stack: inspect.stack) -> list:
    non_system_frames = list()
    if not isinstance(stack, Iterable):
        raise TypeError(f'\'{stack}\' is not iterable')
    for frame in stack:
        caller = get_caller_from_(frame)
        if not_system_(caller):
            non_system_frames.append(frame)
    return non_system_frames


def reverse_order_of_elements_in_(stack_call_string: str, delimiter: str) -> str:
    reversed_list, reversed_list_with_delimiter = list(), list()
    for element in stack_call_string.split(delimiter):
        reversed_list.append(element)
    reversed_list.reverse()
    for sorted_element in reversed_list:
        reversed_list_with_delimiter.extend([delimiter, sorted_element])
    return '.'.join(reversed_list_with_delimiter)


def valid_string_(test_val) -> bool:
    try:
        return True if isinstance(test_val, str) else False
    except Exception as e_err:
        for arg in e_err.args:
            print(arg)


def _log_deprecated(minimalog: MinimalLog, msg: str, event_completed=None,
                    level=logging.INFO, announcement=False,
                    dump_call_stack=False) -> None:
    msg = msg if valid_string_(msg) else str(msg)
    events_to_log = [msg]
    dump_call_stack = True if level == logging.ERROR else False
    if dump_call_stack:
        function_names_in_call_stack = get_function_names_in_call_stack()
        stack_call_string, delimiter = '', ' > '
        for function_name in function_names_in_call_stack:
            if stack_call_string == '':
                stack_call_string = function_name  # build root of string
                continue
            stack_call_string += delimiter + function_name  # append onto string
        # sort the built string
        stack_call_string = reverse_order_of_elements_in_(stack_call_string, delimiter)
        events_to_log.append(stack_call_string)
        call_stack_above_logger = get_call_stack_above_logger(function_names_in_call_stack)
        call_stack_above_logger.reverse()  # sort so that the for loop walks "down" the call stack
        call_stack_log_msg = ''  # start building message here
        for num, call in enumerate(call_stack_above_logger):
            if call == 'x':
                break  # TODO does this hide calls 'below' the logger on the stack call list?
            call_stack_log_msg = f'{call_stack_log_msg} \n\t\t\t\t{call_stack_above_logger[num]}'
            if not num:  # num == 0
                call_stack_log_msg = f'\n\t\tdumping call stack for {call_stack_above_logger[num]}'
        if announcement:
            call_stack_log_msg = announce_(call_stack_log_msg)
        events_to_log.append(call_stack_log_msg)
    for index, msg in enumerate(events_to_log):
        if event_completed is None:
            continue
        events_to_log[index] = f'success : {msg}' if event_completed else f'attempt : {msg}'
    for index, msg in enumerate(events_to_log):
        if announcement:
            minimalog.logger.log(level=level, msg=announce_(msg))
            print(announce_(msg))
            if events_to_log[-1] == msg:
                return
        minimalog.logger.log(level=level, msg=msg)
        print(msg)
    return


if __name__ == '__main__':
    from ascii_art.event_wrappers import *
    sl = MinimalLog()
    # sl.clean_up()
else:
    from .ascii_art.event_wrappers import *
