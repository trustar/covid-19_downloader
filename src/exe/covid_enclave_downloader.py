# encoding = utf-8

""" The COVID enclave downloader app's main file. """

import json
from collections import OrderedDict
from logging import getLogger
from os.path import dirname, abspath, join
from typing import TYPE_CHECKING

from trustar import TruStar

if TYPE_CHECKING:
    from typing import *
    from trustar import Report, Indicator, Tag

_COVID_ENCLAVE_ID = 'b0a7be7b-a847-4597-9e1d-20ae18c344ea'
_EARLIEST_REPORT_UPDATED_TIMESTAMP = 1584082800000

_THIS_DIRECTORY = dirname(abspath(__file__))

_PRIVATE_CONFIG_DIR = join(_THIS_DIRECTORY, '..', '..', 'config_file',
                           'private')
_CONFIG_FILE_NAME = 'trustar.conf'
_CONFIG_FILE_PATH = join(_PRIVATE_CONFIG_DIR, _CONFIG_FILE_NAME)
_CONFIG_ROLE = 'trustar'

_OUTPUT_DIR = join(_THIS_DIRECTORY, '..', '..', 'output')

_LOG_DIR = join(_THIS_DIRECTORY, '..', '..', 'logs')

logger = getLogger(__name__)

class _ReportPackage(object):
    """ Data Struct to keep a Report, its Tags, and its Indicators together. """
    def __init__(self,
                 report,                               # type: Report
                 tag_names,                            # type: List[str]
                 indicators                            # type: List[Indicator]
                 ):
        self.report = report
        self.tag_names = tag_names
        self.indicators = indicators

    def to_dict(self):  # type: (_ReportPackage) -> OrderedDict
        """ Converts the report, its indicators, and its tags to a JSON str.
        """
        d = OrderedDict()
        d['report'] = self.report.to_dict()
        d['report_tags'] = self.tag_names
        d['indicators'] = [indicator.to_dict(remove_nones=True) for
                           indicator in self.indicators]
        return d

def _main():

    ts = _build_trustar_client()                          # type: TruStar
    reports = _get_reports(ts)                            # type: List[Report]

    for report in reports:                             # type: Report
        package = _build_package(ts, report)            # type: _ReportPackage
        filename = _filename_from(package.report)       # type: str
        path = _path_from(filename)                     # type: str
        _write_to_file(package.to_dict(), path)

def _build_trustar_client():                             # type: () -> TruStar
    """ Builds the TruSTAR Client. """
    return TruStar(config_file=_CONFIG_FILE_PATH,
                   config_role=_CONFIG_ROLE)

def _get_reports(ts):                        # type: (TruStar) -> List[Report]
    """ Builds a list of the reports in the enclave. """
    gen = _get_report_gen_from(ts)
    return _report_gen_to_list(gen)

def _get_report_gen_from(ts):           # type: (TruStar) -> Generator[Report]
    """ Builds the report generator. """
    return ts.get_reports(enclave_ids=[_COVID_ENCLAVE_ID],
                          from_time=_EARLIEST_REPORT_UPDATED_TIMESTAMP)

def _report_gen_to_list(gen                     # type: Generator[Report]
                        ):                      # type: (...) -> List[Report]
    """ Downloads reports from generator to list. """
    _log_starting_report_download()
    reports = []
    for report in gen:
        reports.append(report)
        _log_added_report(report)
    _log_done_downloading_reports(len(reports))
    return reports

def _log_starting_report_download():
    """ Writes log message. """
    logger.info("Starting report download.")

def _log_added_report(report):                        # type: (Report) -> None
    """ Writes log message. """
    msg = ("added report, time: '{}', ID:  '{}'"
           .format(report.updated, report.id))
    logger.debug(msg)

def _log_done_downloading_reports(n_reports):            # type: (int) -> None
    """ Writes log message. """
    msg = ("Done downloading reports.  Downloaded '{}' reports."
           .format(str(n_reports)))
    logger.info(msg)


def _build_package(ts,                         # type: TruStar
                   report                      # type: Report
                   ):                          # type: (...) -> _ReportPackage
    """ Builds ReportPackage object. """
    _log_building_package_for(report)
    package =  _ReportPackage(report,
                             _get_tags(ts, report),
                             _get_indicators(ts, report))
    _log_done_building_package_for(report)
    return package

def _log_building_package_for(report):                # type: (Report) -> None
    """ Writes log message. """
    msg = "Building package for report ID '{}'.".format(report.id)
    logger.info(msg)

def _log_done_building_package_for(report):           # type: (Report) -> None
    """ Writes log message. """
    msg = "Done building package for report ID '{}'".format(report.id)
    logger.info(msg)


def _get_indicators(ts,                       # type: TruStar
                    report                    # type: Report
                    ):                        # type: (...) -> List[Indicator]
    """ Builds a list of the report's indicators. """
    _log_fetching_indicators_for(report)
    indicators = []
    try:
        gen = ts.get_indicators_for_report(report.id)  # type: Generator[Indicator]
        for indicator in gen:
            indicators.append(indicator)
        if indicators:
            _log_found_indicators_for(report, len(indicators))
        else:
            _log_has_no_indicators(report)

    except Exception as e:
        _log_fetching_indicators_failed_for(report, e)

    return indicators

def _log_fetching_indicators_for(report):             # type: (Report) -> None
    """ Writes log message. """
    msg = ("Fetching indicators for report updated '{}', title '{}', id "
           "'{}'".format(report.updated, report.title, report.id))
    logger.info(msg)

def _log_found_indicators_for(report,                          # type: Report
                              n_indicators                     # type: int
                              ):
    """ Writes log message. """
    msg = ("Done fetching indicators for report id '{}'.  Found '{}' "
           "indicators.".format(report.id, str(n_indicators)))
    logger.info(msg)

def _log_has_no_indicators(report):                   # type: (Report) -> None
    """ Writes log message. """
    msg = ("Found no indicators for report ID '{}'.".format(report.id))
    logger.info(msg)

def _log_fetching_indicators_failed_for(report,             # type: Report
                                        e                   # type: Exception
                                        ):
    """ Writes log message. """
    msg = ("Fetching indicators failed for report ID '{}'.  Exception "
           "message:  '{}'.".format(report.id, e))
    logger.error(msg)

def _get_tags(ts, report):              # type: (TruStar, Report) -> List[str]
    """ Builds a list of the report's tags. """
    tags = _fetch_tags(ts, report)
    tag_names = _extract_tag_names_from(tags, report)
    return tag_names

def _fetch_tags(ts,                                 # type: TruStar
                report                              # type: Report
                ):                                  # type: (...) -> List[Tag]
    """ Try/except wrapper around API call to get tags. """
    _log_fetching_tags_for(report)
    try:
        tags = ts.get_enclave_tags(report.id)                # type: List[Tag]
        _log_fetching_tags_succeeded_for(report)
        return tags
    except Exception as e:
        _log_fetching_tags_failed_for(report, e)
        return []

def _log_fetching_tags_for(report):                   # type: (Report) -> None
    """ Writes log message. """
    msg = ("Fetching tags for report ID '{}'.".format(report.id))
    logger.info(msg)

def _log_fetching_tags_succeeded_for(report):
    """ Writes log msg. """
    msg = ("Fetch tags API call succeeded for report ID '{}'."
           .format(report.id))
    logger.info(msg)

def _log_fetching_tags_failed_for(report,               # type: Report
                                  e                     # type: Exception
                                  ):
    """ Writes log message. """
    msg = ("Error:  Fetching tags failed for report ID '{}'.  Exception "
           "message:  '{}'.".format(report.id, e))
    logger.error(msg)


def _extract_tag_names_from(tags, report):
    """ Gets tag names from Tag objects. """
    if tags:
        tag_names = [tag.name for tag in tags]
        _log_found_tags_for(report, tag_names)
        return tag_names
    else:
        _log_has_no_tags(report)
        return []

def _log_found_tags_for(report,                             # type: Report
                        tag_names                           # type: List[str]
                        ):
    """ Writes log message. """
    msg = ("Found tags for report ID '{}':  '{}'."
           .format(report.id, str(tag_names)))
    logger.info(msg)

def _log_has_no_tags(report):                         # type: (Report) -> None
    """ Writes log message. """
    msg = ("Report ID '{}' has no tags.".format(report.id))
    logger.info(msg)

def _filename_from(report):                            # type: (Report) -> str
    """ Builds the filename from the report. """
    filename = '{}_{}_{}.json'.format(report.updated, report.title, report.id)
    return filename

def _path_from(filename):                                 # type: (str) -> str
    """ Builds the output file path. """
    return join(_OUTPUT_DIR, filename)

def _write_to_file(report_dict, filepath):  # type: (OrderedDict, str) -> None
    """ Writes the report to file. """
    _log_writing_to(filepath)
    with open(filepath, 'w') as f:
        json.dump(report_dict, f, indent=4)
    _log_done_writing_file()

def _log_writing_to(filepath):
    """ Writes log message. """
    logger.info("Writing to file '{}'.".format(filepath))

def _log_done_writing_file():
    """ Writes log message. """
    logger.info("Done writing file.")

if __name__ == "__main__":

    _main()
