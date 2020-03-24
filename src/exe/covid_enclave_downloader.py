# encoding = utf-8

""" The COVID enclave downloader app's main file. """

from os.path import dirname, abspath, join

from trustar_enclave_downloader import EnclaveDownloader
from trustar import TruStar

_THIS_DIRECTORY = dirname(abspath(__file__))
_COVID_ENCLAVE_ID = 'b0a7be7b-a847-4597-9e1d-20ae18c344ea'
_EARLIEST_REPORT_UPDATED_TIMESTAMP = 1584082800000


def _build_trustar_client():                            # type: () -> TruStar
    return TruStar(config_file='trustar.conf',
                   config_role='trustar')


if __name__ == "__main__":
    output_dir = join(_THIS_DIRECTORY, '..', 'output')
    ts = _build_trustar_client()
    downloader = EnclaveDownloader(ts,
                                   output_dir,
                                   _COVID_ENCLAVE_ID,
                                   _EARLIEST_REPORT_UPDATED_TIMESTAMP)
    downloader.download()