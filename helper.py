import grp
import os
import pwd
from datetime import datetime

from termcolor import cprint

from constants import *


def check_dir_exists(directory):
    return os.path.isdir(directory)


def check_file_exists(file_path):
    return os.path.isfile(file_path)


def file_dir(file_path):
    return os.path.dirname(file_path)


def is_asset_exists(path, is_dir, file_name):
    check = check_dir_exists(path) if is_dir else check_file_exists(path)
    if check:
        cprint(file_name + ' exist', COLOR_SUCCESS)
        return True
    cprint(file_name + ' does not exist', COLOR_ERROR)
    return False


def is_outside_monitor(monitor, file_path, file_name):
    if file_dir(file_path) in monitor:
        cprint(file_name + ' is inside monitor', COLOR_ERROR)
        return False
    cprint(file_name + ' is outside monitor', COLOR_SUCCESS)
    return True


def file_check(file_path, file_name, is_initialization):
    is_asset_exist = is_asset_exists(file_path, False, file_name)
    if is_asset_exist and is_initialization:
        while True:
            cprint('Do you want to override ' + file_name + '? ', COLOR_ERROR)
            input_data = str(raw_input())
            if input_data == 'no':
                exit()
            elif input_data == 'yes':
                break
            else:
                cprint('Please enter yes or no', COLOR_INFO)
    elif not is_initialization and not is_asset_exist:
        exit()
    return True


def collect_info(path):
    stat_info = os.stat(path)
    info = {
        STAT_USER: pwd.getpwuid(stat_info.st_uid)[0],
        STAT_GROUP: grp.getgrgid(stat_info.st_gid)[0],
        STAT_MODE: oct(stat_info.st_mode & 07777),
        STAT_MOD_DATE: datetime.fromtimestamp(stat_info.st_mtime).date().__str__()
    }

    if not os.path.isdir(path):
        info[STAT_SIZE] = stat_info.st_size
        from hash import hashing
        info[STAT_DIGEST] = hashing(path)

    return info
