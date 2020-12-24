import logging


class LogTools(logging.getLoggerClass()):
    def __init__(self):
        try:
            self.logger = logging.getLogger(__name__)
            self.log_format, self.time_format = self.get_log_and_time_format_strings()
            self.configure()
        except RuntimeError:
            raise RuntimeError

    def configure(self):
        try:
            logging.basicConfig(filename=self.get_log_filename(), filemode='a')
        except RuntimeError:
            raise RuntimeError

    def demo(self):
        self.log_info_event("running demonstration function")

    def log_info_event(self, msg):
        try:
            self.logger.log(level=logging.INFO, msg=msg)
        except RuntimeError:
            raise RuntimeError

    @staticmethod
    def get_log_filename() -> str:
        return "event.log"

    def get_log_and_time_format_strings(self):
        return self.get_log_format(), self.get_time_format()

    def get_log_format(self):
        # reference : https://docs.python.org/3/library/logging.html#logrecord-attributes
        return "%(asctime)s : %(name)s : %(levelname)s in %(filename)s from %(funcName)s : %(message)s"
        
    def get_time_format(self):
        # reference : https://docs.python.org/3/library/time.html#time.strftime
        return "%Y-%m-%d, %H:%M:%S"
    

if __name__ == '__main__':
    lt = LogTools()
    lt.demo()
