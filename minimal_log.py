from inspect import FrameInfo
import inspect
import logging
import os
import pathlib2

ERROR_LEVELS = (logging.INFO, logging.DEBUG,
                logging.WARNING, logging.ERROR)


class MinimalLog:
    def __init__(self, logger_name=None, debug=False):
        self.INFO, self.DEBUG, self.WARNING, self.ERROR = ERROR_LEVELS
        try:
            if logger_name:
                self.logger = logging.getLogger(logger_name)  # get logger
            else:
                self.logger = logging.getLogger()  # get root logger
            self.log_format, self.time_format = self.get_format_strings()  # time_format not used yet
            self.configure(overwrite=False)
            if debug:
                self.__debug()
        except Exception as e_err:
            self.log_exception(e_err, level=self.ERROR)

    def clean_up(self):
        """
        deletes all files with extension .log in the project directory and below
        :return: None
        """
        try:
            log_files = self.find_all_files_with_extension('.log')
            self.delete_list_of_files(log_files)
        except Exception as es_err:
            self.log_exception(es_err, level=self.ERROR)

    def configure(self, overwrite=True):
        """
        :param overwrite: determines if existing log files are overwritten, or appended
        :return: None
        """
        filemode = self.get_log_filemode_append()
        if overwrite:
            filemode = self.get_log_filemode_overwrite()
        try:
            logging.basicConfig(filename=self.get_log_filename(),
                                filemode=filemode,
                                level=self.get_default_level(),
                                format=self.log_format)
        except Exception as e_err:
            self.log_exception(e_err, level=self.ERROR)

    def delete_list_of_files(self, files_to_delete: list):
        """
        :param files_to_delete: self-documenting
        :return: None
        """
        try:
            for file in files_to_delete:
                os.remove(file)
        except Exception as e_err:
            self.log_exception(e_err, level=self.ERROR)

    def find_all_files_with_extension(self, extension='.log') -> list:
        """
        :param extension: the file extension to find
        :return: a list of files with the extension
        """
        list_of_log_files = list()
        try:
            for root, directories, files in os.walk(os.getcwd()):
                for file in files:
                    if file.endswith('.log'):
                        list_of_log_files.append(pathlib2.Path(root, file).absolute())
            return list_of_log_files
        except Exception as e_err:
            self.log_exception(e_err, level=self.ERROR)

    def get_default_level(self) -> int:
        """
        :return: the default logging level, usually INFO
        """
        try:
            return logging.INFO
        except Exception as e_err:
            self.log_exception(e_err, level=self.ERROR)

    def get_format_strings(self):
        """
        basic configuration options
        :return: a tuple of two configuration strings
        """
        return self.get_format_string_for_log(), self.get_format_string_for_time()

    @staticmethod
    def get_format_string_for_log():
        """
        :return: a hardcoded string, in the future this could be re-worked but for now, who cares
        """
        # reference : https://docs.python.org/3/library/logging.html#logrecord-attributes
        return "PID : %(process)d : %(asctime)s : %(name)s : %(levelname)s : %(funcName)s : %(lineno)d : %(message)s"

    @staticmethod
    def get_format_string_for_time():
        """
        :return: a hardcoded string, in the future this could be re-worked but for now, who cares
        """
        # reference : https://docs.python.org/3/library/time.html#time.strftime
        return "%Y-%m-%d, %H:%M:%S"

    @staticmethod
    def get_log_filemode_append() -> str:
        """
        :return: a hardcoded string, in the future this could be re-worked but for now, who cares
        """
        return 'a'

    @staticmethod
    def get_log_filemode_overwrite() -> str:
        """
        :return: a hardcoded string, in the future this could be re-worked but for now, who cares
        """
        return 'w'

    @staticmethod
    def get_log_filename() -> str:
        """
        :return: a hardcoded string, in the future this could be re-worked but for now, who cares
        """
        return "event.log"

    def log_exception(self, exception, level=logging.ERROR):
        # TODO bug, doesn't work, exceptions exit before call
        """
        :param exception: the exception from which details are extracted and written to the log file
        :param level: manual override of the default logging level
        :return:  None
        """
        try:
            self.logger.exception(msg=str(exception), level=level)
        except Exception as e_err:
            print(e_err)

    def log_event(self, event,
                  event_completed=None,
                  level=logging.INFO,
                  announce=False,
                  log_call_stack=False):
        # TODO bug.. no matter where this function is located it always says it's own name for %(funcName)s in log..
        # TODO ..file. should fix that, would make debugging easier if it called the name of the function calling it
        """
        :param event: event string to be logged
        :param event_completed: whether this is the beginning or end of the event
        :param level: manual override of the default logging level
        :param announce: bool, create a visible distinction in the log file
        :param log_call_stack: bool, set to True for more spam about function calls
        :return: None
        """
        if not _string_is_valid(event):
            try:
                event = str(event)
            except Exception as e_err:
                print(e_err)

        events_to_log = [event]
        if log_call_stack:
            function_names_in_call_stack = _get_function_names_in_call_stack()
            stack_call_string = ''
            for function_name in function_names_in_call_stack:
                if stack_call_string == '':
                    stack_call_string = function_name
                    continue
                stack_call_string += ' < ' + function_name
            events_to_log.append(stack_call_string)

        for index, event in enumerate(events_to_log):
            if event_completed is True:
                event = 'success : ' + event
            elif event_completed is False:
                event = 'attempt : ' + event
            events_to_log[index] = event

        try:
            for index, event in enumerate(events_to_log):
                if announce:
                    self.logger.log(level=level, msg=ANNOUNCE(event))
                    print(ANNOUNCE(event))
                    if events_to_log[-1] == event:
                        return
                self.logger.log(level=level, msg=event)
                print(event)
                return
        except Exception as e_err:
            print(e_err)

    def __debug(self):
        """
        a place to run test code when developing
        :return: None
        """
        self.log_event(event='meaningless debug event', event_completed=False, announce=True)
        for i in range(9):
            self.log_event(event='intermediate event number {}'.format(i), log_call_stack=True)
        self.log_event(event='meaningless debug event', event_completed=True, announce=True)


def _get_caller_name_from_(frame: FrameInfo) -> str:
    try:
        caller_name = ''
        frame_at_function_name_index = frame[3]
        if frame_at_function_name_index is not None:
            caller_name = frame_at_function_name_index
        return caller_name
    except Exception as e_err:
        print(e_err)


def _get_function_names_in_call_stack():
    try:
        stack = _get_stack(filter_system_frames=True)
        function_names_in_call_stack = list()
        for frame in stack:
            caller = _get_caller_name_from_(frame)
            function_names_in_call_stack.append(caller)
        return function_names_in_call_stack
    except Exception as e_err:
        print(e_err)


def _get_stack(filter_system_frames=True) -> inspect.stack:
    try:
        stack = inspect.stack()
        if filter_system_frames:
            stack = _remove_system_frames_from_(stack)
        return stack
    except Exception as e_err:
        print(e_err)


def _get_stack_depth(stack) -> int:
    try:
        assert stack, 'assertion failed, stack has Falsy value'
        stack_depth_count = 0
        for _ in stack:
            stack_depth_count += 1
        return stack_depth_count
    except Exception as e_err:
        print(e_err)


def _is_non_system_(caller_name: str) -> bool:
    """
    valid in the current context means, "non-system" calls
    :param caller_name: a caller name, can be a function, module, dunder, etc
    :return: bool, True = valid, False = invalid
    """
    system_calls = [
        '_call_with_frames_removed',
        '_exec',
        'exec_module',
        'execfile',
        '_find_and_load',
        '_find_and_load_unlocked',
        '_load_unlocked'
                    ]
    try:
        if caller_name is None:  # filter None
            return False
        if caller_name in system_calls:
            return False
        if caller_name.endswith('__') or caller_name.endswith('>'):  # filter dunder, <module>,
            return False
        return True
        pass
    except Exception as e_err:
        print(e_err)


def _remove_system_frames_from_(stack: inspect.stack) -> list:
    try:
        non_system_frames = list()
        for frame in stack:
            caller_name = _get_caller_name_from_(frame)
            if _is_non_system_(caller_name):
                non_system_frames.append(frame)
        return non_system_frames
    except Exception as e_err:
        print(e_err)


def _string_is_valid(string_to_check):
    """
    :param string_to_check: self documenting
    :return: bool, valid string or not
    """
    try:
        if isinstance(string_to_check, str):
            return True
        return False
    except Exception as e_err:
        print(e_err)


if __name__ == '__main__':
    from data_src.CONSTANTS import *
    sl = MinimalLog(debug=True)
    pass
else:
    from .data_src.CONSTANTS import *
