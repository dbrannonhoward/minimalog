from minimal_log import MinimalLog
ml1 = MinimalLog(__name__)  # this gets the correct logger
ml2 = MinimalLog()  # this gets the incorrect logger


def an_imported_function():
    ml1.log_info_event('child logger in import, correct info event from ' + __name__)
    ml2.log_info_event('root logger in import, incorrect info event from ' + __name__)


an_imported_function()
