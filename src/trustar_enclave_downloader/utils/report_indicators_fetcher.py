# encoding = utf-8

from logging import getLogger

from .type_checking import *

logger = getLogger(__name__)

class ReportIndicatorsFetcher(object):
    """ Fetches indicators for a report. """

    def __init__(self,
                 report                     # type: Report
                 ):
        self._report = report               # type: Report

    @staticmethod
    def for_report(report):        # type: (Report) -> ReportIndicatorsFetcher
        """ Factory method, builds a fetcher for a report. """
        return ReportIndicatorsFetcher(report)

    def fetch_using(self, ts):            # type: (TruStar) -> List[Indicator]
        """ Fetches the report's indicators from Station. """
        indicators = self._get_gen(ts)            # type: Generator[Indicator]
        indicators = self._gen_to_list(indicators)  # type: List[Indicator]
        return indicators

    def _get_gen(self, ts):          # type: (TruStar) -> Generator[Indicator]
        """ Gets the generator from TruSTAR python SDK. """
        return ts.get_indicators_for_report(self._report.id)

    def _gen_to_list(self,
                     indicators              # type: Generator[Indicator]
                     ):                      # type: (...) -> List[Indicator]
        """ Try/except wrapper for converter. Catches and logs any
        API call failures encountered while downloading the indicators
        through the generator, to the list. """
        try:
            return self._convert_to_list(indicators)
        except Exception as e:
            self._log_indicator_fetch_failure(e)
            return False

    def _convert_to_list(self,
                         indicators           # type: Generator[Indicator]
                         ):                   # type: (...) -> List[Indicator]
        """ Converts the gen to list. """
        indicators_list = []
        for indicator in indicators:
            indicators_list.append(indicator)
        return indicators_list

    def _log_indicators_fetch_failure(self, e):  # type: (Exception) -> None
        msg = FailureMessages.INDICATOR_FETCH_FAILURE.format(
            self._report.id, self._report.title, e)
        logger.error(msg)


class FailureMessages(object):
    """ A class to hold failure messages for logging and exceptions. """
    INDICATOR_FETCH_FAILURE = (
        "Error while fetching indicators for report ID '{}', title '{}'.  "
        "Exception Message:  '{}'.  Bypassing and continuing.")