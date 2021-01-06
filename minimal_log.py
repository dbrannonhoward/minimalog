import logging
import os
import pathlib2


class MinimalLog:
    def __init__(self, logger_name=None, debug=False):
        self.INFO, self.DEBUG, self.WARN, self.WARNING, self.ERROR = logging.INFO, \
                                                                     logging.DEBUG, \
                                                                     logging.WARN, \
                                                                     logging.WARNING, \
                                                                     logging.ERROR
        try:
            if logger_name:
                self.logger = logging.getLogger(logger_name)  # get logger
            else:
                self.logger = logging.getLogger()  # get the root logger
            self.log_format, self.time_format = self.get_format_strings()  # time_format not used yet
            self.configure(overwrite=False)
            if debug:
                self.__debug()
        except RuntimeError as r_err:
            self.log_exception(r_err)

    def clean_up(self):
        try:
            log_files = self.find_all_files_with_extension('.log')
            MinimalLog.delete_list_of_files(log_files)
        except OSError as os_err:
            self.log_exception(os_err)

    def configure(self, overwrite=True):
        if overwrite:
            filemode = self.get_log_filemode_overwrite()
        else:
            filemode = self.get_log_filemode_append()
        try:
            logging.basicConfig(filename=self.get_log_filename(),
                                filemode=filemode,
                                level=self.get_default_level(),
                                format=self.log_format)
        except RuntimeError as r_err:
            self.log_exception(r_err)

    def delete_list_of_files(self, files_to_delete: list):
        for file in files_to_delete:
            try:
                os.remove(file)
            except OSError as o_err:
                self.log_exception(o_err)

    def find_all_files_with_extension(self, extension='.log') -> list:
        list_of_log_files = list()
        try:
            for root, directories, files in os.walk(os.getcwd()):
                for file in files:
                    if file.endswith('.log'):
                        list_of_log_files.append(pathlib2.Path(root, file).absolute())
            return list_of_log_files
        except OSError as o_err:
            self.log_exception(o_err)

    def get_default_level(self) -> int:
        try:
            return logging.INFO
        except ValueError as v_err:
            self.log_exception(v_err)

    def get_format_strings(self):
        return self.get_format_string_for_log(), self.get_format_string_for_time()

    @staticmethod
    def get_format_string_for_log():
        # reference : https://docs.python.org/3/library/logging.html#logrecord-attributes
        return "%(asctime)s : %(levelname)s : %(name)s : %(message)s"

    @staticmethod
    def get_format_string_for_time():
        # reference : https://docs.python.org/3/library/time.html#time.strftime
        return "%Y-%m-%d, %H:%M:%S"

    @staticmethod
    def get_log_filemode_append() -> str:
        return 'a'

    @staticmethod
    def get_log_filemode_overwrite() -> str:
        return 'w'

    @staticmethod
    def get_log_filename() -> str:
        return "event.log"

    def log_exception(self, exception, level=logging.ERROR):
        # TODO bug, doesn't work, exceptions exit before call
        try:
            self.logger.exception(msg=str(exception), level=level)
        except OSError as o_err:
            print(o_err)

    def log_event(self, event, event_completed=None, level=logging.INFO,
                  announce=False):
        if not self.string_is_valid(event):
            try:
                event = str(event)
            except TypeError as t_err:
                self.log_exception(t_err)
        if event_completed is True:
            event = 'success : ' + event
        elif event_completed is False:
            event = 'attempt : ' + event
        try:
            if announce:
                self.logger.log(level=level, msg=ANNOUNCE(event))
                return
            self.logger.log(level=level, msg=event)
            return
        except RuntimeError as r_err:
            self.log_exception(r_err)

    def string_is_valid(self, string_to_check):
        try:
            if isinstance(string_to_check, str):
                return True
            return False
        except TypeError as t_err:
            self.log_exception(t_err)

    def __debug(self):
        self.log_event(event='meaningless debug event',
                       event_completed=False,
                       announce=True)
        for i in range(9):
            self.log_event(event='intermediate event number {}'.format(i))
        self.log_event(event='meaningless debug event',
                       event_completed=True,
                       announce=True)


if __name__ == '__main__':
    from data_src.CONSTANTS import ANNOUNCE
    sl = MinimalLog(debug=True)
else:
    from .data_src.CONSTANTS import ANNOUNCE
