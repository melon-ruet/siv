import argparse

from termcolor import cprint

from constants import *
from hash import is_hash_supported
from helper import is_asset_exists, is_outside_monitor, file_check
from initialization import exec_initialization
from verification import Verification

parser = argparse.ArgumentParser()
parser.add_argument("-i", action="store_true", default=False)
parser.add_argument("-v", action="store_true", default=False)
parser.add_argument("-D", "--Monitor", help="Monitor Directory")
parser.add_argument("-V", "--Verification", help="Verification Directory")
parser.add_argument("-R", "--Report", help="Report file name")
parser.add_argument("-H", "--hash", help="hash code SHA-1", type=str, default="SHA-1")
args = parser.parse_args()

monitor = args.Monitor
verification = args.Verification
report = args.Report

if not (monitor and verification and report):
    cprint('Please provide ' + monitor_name + ', ' + verification_name + ' and ' + report_name, COLOR_INFO)
    exit()

if not is_asset_exists(monitor, True, monitor_name):
    exit()
if not is_outside_monitor(monitor, verification, verification_name):
    exit()
if not is_outside_monitor(monitor, report, report_name):
    exit()

if args.i and args.v:
    cprint('Initialization and Verification can not perform together', COLOR_ERROR)
elif args.i:
    file_check(verification, verification_name, True)
    file_check(report, report_name, True)
    if not is_hash_supported(args.hash):
        exit()
    exec_initialization(monitor=monitor, verification=verification, report=report)
    cprint('Initialization mode completed', COLOR_SUCCESS)
elif args.v:
    file_check(verification, verification_name, False)
    ver = Verification(monitor=monitor, verification=verification, report=report)
    ver.execute()
    cprint('Verification mode completed', COLOR_SUCCESS)
