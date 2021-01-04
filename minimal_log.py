from data_src.CONSTANTS import ANNOUNCE
import logging
import os
import pathlib2


class MinimalLog:
    def __init__(self, logger_name=None, debug=False):
        self.INFO, self.DEBUG, self.WARN, self.WARNING = logging.INFO, \
                                                         logging.DEBUG, \
                                                         logging.WARN, \
                                                         logging.WARNING
        try:
            if logger_name:
                self.logger = logging.getLogger(logger_name)  # get logger
            else:
                self.logger = logging.getLogger()  # get the root logger
            self.log_format, self.time_format = self.get_format_strings()  # time_format not used yet
            self.configure(overwrite=False)
            if debug:
                self._debug()
        except RuntimeError:
            raise RuntimeError

    @classmethod
    def clean_up(cls):
        log_files = MinimalLog.find_all_files_with_extension('.log')
        MinimalLog.delete_list_of_files(log_files)

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
        except RuntimeError:
            raise RuntimeError

    @classmethod
    def delete_list_of_files(cls, files_to_delete: list):
        for file in files_to_delete:
            try:
                os.remove(file)
            except OSError:
                raise OSError

    @classmethod
    def find_all_files_with_extension(cls, extension='.log') -> list:
        list_of_log_files = list()
        for root, directories, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith('.log'):
                    list_of_log_files.append(pathlib2.Path(root, file).absolute())
        return list_of_log_files

    @staticmethod
    def get_default_level() -> int:
        return logging.INFO

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

    def log_event(self, event, event_completed=None, level=logging.INFO, announce=False):
        if not self.string_is_valid(event):
            try:
                event = str(event)
            except TypeError:
                raise TypeError
        if event_completed is True:
            event = 'success : ' + event
        elif event_completed is False:
            event = 'attempt : ' + event
        try:
            if announce:
                event = ANNOUNCE(event)
            self.logger.log(level=level, msg=event)
        except RuntimeError:
            raise RuntimeError

    @staticmethod
    def string_is_valid(string_to_check):
        if isinstance(string_to_check, str):
            return True
        return False

    def _debug(self):
        for i in range(9):
            if i == 0:
                self.log_event(event='opening announcement test', event_completed=False, announce=True)
            elif i == 8:
                self.log_event(event='closing announcement test', event_completed=True, announce=True)
            else:
                self.log_event(event='did thing {}'.format(i))


if __name__ == '__main__':
    sl = MinimalLog(debug=True)
