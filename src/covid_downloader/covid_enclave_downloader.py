# encoding = utf-8

""" Script to jsonify each report and drop it into a file on the localhost. """

from os.path import join, abspath, dirname
from typing import TYPE_CHECKING
from logging import getLogger

from trustar import TruStar
from trustar.models.enum import IdType

if TYPE_CHECKING:
    from typing import *
    from trustar import Report, Tag, Indicator




logger = getLogger(__name__)


class FailureMessages(object):
    """ A class to hold failure messages. """
    REPORT_DOWNLOAD_FAILURE = ("Failure encountered while downloading "
                               "reports.  Exception messaage: '{}'.  "
                               "Terminating.")

class CovidDownloader(object):
    """ Stores JSON versions of reports, indicators, and tags in files. """

    def __init__(self,
                 ts,                                           # type: TruStar
                 output_dir,                                   # type: str
                 enclave_id,                                   # type: str
                 from_time                                     # type: int
                 ):
        self._ts = ts                                          # type: TruStar
        self._output_dir = output_dir                          # type: str
        self._enclave_id = enclave_id                          # type: str
        self._from_time = from_time                            # type: int


    def go(self):

        reports = self._get_reports()                # type: Generator[Report]

        report_packages = []
        for report in reports:
            report_packages.append(ReportPackage(report))

        for package in report_packages:
            package.fetch_indicators()
            package.fetch_report_tags()
            package.fetch_indicator_tags

        reports_package = ReportPackages.from_get_endpoint(reports)

        return reports_package


            self._write_output_file(report.to_dict())

    def _get_reports(self,
                     params):                    # type: () -> Generator[
        # Report]
        """ Builds the report generator. """
        reports_list = []
        reports = self._ts.get_reports(
            enclave_ids=[self._enclave_id],
            from_time=self._from_time)

        try:
            for report in reports:
                reports_list.append(report)
        except Exception as e:
            self._log_report_download_failure(e)
            raise ReportDownloadFailure(e)

    def _log_report_download_failure(self, e):
        logger.error(self.REPORT_DOWNLOAD_FAILURE_MSG.format(e))




class ReportPackage(object):






    def _get_indicators(self, report):     # type: (Report) -> List[Indicator]
        """ Builds the list of indicators. """

        indicators = self._ts.get_indicators_for_report(report.id)

        try:
            return list(indicators)
        except Exception as e:



        report_tags = ts.get_enclave_tags(
            report.id, id_type=IdType.INTERNAL)  # type: List[Tag]


        d = report.to_dict()

        report_file_path = join(OUTPUT_DIR, filename)

        with open(report_file_path,'w') as f:


class ReportDownloadFailure(Exception):
    def __init__(self, e):
        msg = FailureMessages.REPORT_DOWNLOAD_FAILURE.format(e)
        super().__init__(msg)


