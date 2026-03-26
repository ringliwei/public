import argparse
import logging
import logging.handlers as h
import os
import pathlib

FILE_NAME = os.path.basename(__file__)

SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))

SCRIPT_DIR = os.path.split(os.path.realpath(__file__))[0]

LOG_DIR = pathlib.Path(f"{SCRIPT_DIR}/logs")

HOME_PATH = os.path.expandvars('$HOMEPATH')

APPDATA_PATH = os.path.expandvars('$APPDATA')

if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    handlers=[logging.StreamHandler(), h.RotatingFileHandler(f'{LOG_DIR}/{FILE_NAME}.log', encoding='utf8')])


def command_line():
    parser = argparse.ArgumentParser()

    parser.description = 'This is a tool scaffold.'

    parser.add_argument(
        "-v", "--version-name",
        help='VersionName',
        required=False,
        type=str
    )

    parser.add_argument(
        "-p", "--with-production", help='''production env''', action="store_true")

    parser.add_argument(
        "-d", "--debug", help='''debug mode''', action="store_true")

    args = parser.parse_args()
    version_name = args.version_name if args.version_name else ""
    debug = True if args.debug else False

    logging.debug(f"debug: {debug}") if debug else ""
    logging.debug(f"version_name: {version_name}") if version_name else ""

    return args


if __name__ == "__main__":

    args = command_line()

    logging.info("Hello, World!")
