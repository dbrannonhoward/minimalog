from example_import import an_imported_function
from minimal_log import MinimalLog
ml = MinimalLog()  # this gets the root logger


def a_main_function():
    ml.log_info_event('root logger in main, correct info event from ' + __name__)


a_main_function()
an_imported_function()
