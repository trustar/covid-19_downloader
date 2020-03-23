# encoding = utf-8

""" Script to jsonify each report and drop it into a file on the localhost. """

from os.path import join, abspath, dirname
from typing import TYPE_CHECKING

from trustar import TruStar
from trustar.models.enum import IdType

if TYPE_CHECKING:
    from typing import *
    from trustar import Report, Tag


this_file_abs_dir = dirname(abspath(__file__))
OUTPUT_DIR = join(this_file_abs_dir, '..', 'output')

ts = TruStar(config_file='trustar.conf',
             config_role='trustar')                            # type: TruStar

for report in ts.get_reports(                                # type: Report
    enclave_ids='b0a7be7b-a847-4597-9e1d-20ae18c344ea',
    from_time=1584082800000):


    report_tags = ts.get_enclave_tags(
        report.id, id_type=IdType.INTERNAL)                 # type: List[Tag]

    indicators = ts.get_indicators_for_report(report.id)




    d = report.to_dict()

    report_file_path = join(OUTPUT_DIR, filename)

    with open(report_file_path,'w') as f:
