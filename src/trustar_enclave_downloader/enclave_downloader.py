# encoding = utf-8

""" Script to jsonify each report and drop it into a file on the localhost. """

__all__ = ["CovidDownloader"]

from os.path import join
from logging import getLogger

from trustar_type_checking import *
from trustar.models.enum import IdType

from .utils import ReportPackages



logger = getLogger(__name__)




class EnclaveDownloader(object):
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
        self._report_packages = None            # type: Report

    def download(self):
        """ Downloads all reports, their indicators, report tags, and
        indicator tags. """

        reports = self._get_reports()                # type: Generator[Report]
        report_packages = ReportPackages.from_get_endpoint(reports)
        report_packages.fetch_indicators()
        report_packages.fetch_report_tags()
        report_packages.fetch_indicator_tags()

        self._report_packages = report_packages



    def _get_reports(self):                    # type: () -> Generator[Report]
        """ Builds the report generator. """
        gen = self._get_report_gen()
        reports = self._report_gen_to_list(gen)

    def _get_report_gen(self):
        return self._ts.get_reports(
            enclave_ids=[self._enclave_id],
            from_time=self._from_time)

    def _report_gen_to_list(self,
                            gen                  # type: Generator[Report]
                            ):                   # type: (...) -> List[Report]

        try:
            return self._gen_to_list(gen)
        except Exception as e:
            self._log_report_download_failure(e)
            raise ReportDownloadFailure(e)

    def _gen_to_list(self,
                     gen
                     ):
        """ Converts gen to list. """
        for report in reports:
            reports_list.append(report)

    def _log_report_download_failure(self, e):
        logger.error(self.REPORT_DOWNLOAD_FAILURE_MSG.format(e))


class FailureMessages(object):
    """ A class to hold failure messages. """
    REPORT_DOWNLOAD_FAILURE = ("Failure encountered while downloading "
                               "reports.  Exception messaage: '{}'.  "
                               "Terminating.")











        report_tags = ts.get_enclave_tags(
            report.id, id_type=IdType.INTERNAL)  # type: List[Tag]


        d = report.to_dict()

        report_file_path = join(OUTPUT_DIR, filename)

        with open(report_file_path,'w') as f:


class ReportDownloadFailure(Exception):
    def __init__(self, e):
        msg = FailureMessages.REPORT_DOWNLOAD_FAILURE.format(e)
        super().__init__(msg)


