# encoding = utf-8

from logging import getLogger

from .type_checking import *

logger = getLogger()                                           # type: Logger

class ReportPackage(object):
    """ A class to easily aggregate a report, its tags, its indicators,
    and their tags.  """

    def __init__(self,
                 report                                     # type: Report
                 ):

        self._report = report                 # type: Report
        self._indicators = None               # type: List[Indicator] or None
        self._report_tags = None              # type: List[str] or None

    def fetch_indicators_using(self,
                               ts                            # type: TruStar
                               ):
        """ Hangs the report's indicators. """
        fetcher = ReportIndicatorsFetcher.for_report(self._report)
        self._indicators = fetcher.fetch_using(ts)


