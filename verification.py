import ast
import os
import time

from constants import *
from helper import monitor_name, verification_name, report_name, FILE_KEY, DIR_KEY, collect_info

warnings = []


class Verification:
    monitor, verification, report = None, None, None
    verification_dict = None
    no_of_dirs, no_of_files = 0, 0
    start_time = None

    def __init__(self, monitor, verification, report):
        self.start_time = time.time()
        self.monitor, self.verification, self.report = monitor, verification, report

    def init_verification_dict(self):
        with open(self.verification, 'r') as f:
            self.verification_dict = ast.literal_eval(f.read())

    def stat_check(self, path, file_name=None):
        if file_name:
            stat_old = self.verification_dict[path][FILE_KEY][file_name]
            path = path + '/' + file_name
            stat_new = collect_info(path)
            if stat_old[STAT_SIZE] != stat_new[STAT_SIZE]:
                warnings.append('File size changed from ' + stat_old[STAT_SIZE] +
                                ' to ' + stat_new[STAT_SIZE] + ' of ' + path)

            if stat_old[STAT_DIGEST] != stat_new[STAT_DIGEST]:
                warnings.append('File digest changed from ' + stat_old[STAT_DIGEST] +
                                ' to ' + stat_new[STAT_DIGEST] + ' of ' + path)
        else:
            stat_new = collect_info(path)
            stat_old = self.verification_dict[path][DIR_KEY]

        if stat_old[STAT_USER] != stat_new[STAT_USER]:
            warnings.append('User changed from ' + stat_old[STAT_USER] + ' to ' + stat_new[STAT_USER] + ' of ' + path)

        if stat_old[STAT_GROUP] != stat_new[STAT_GROUP]:
            warnings.append('Group changed from ' + stat_old[STAT_GROUP] +
                            ' to ' + stat_new[STAT_GROUP] + ' of ' + path)

        if stat_old[STAT_MODE] != stat_new[STAT_MODE]:
            warnings.append('Modification access changed from ' + stat_old[STAT_MODE] +
                            ' to ' + stat_new[STAT_MODE] + ' of ' + path)

        if stat_old[STAT_MOD_DATE] != stat_new[STAT_MOD_DATE]:
            warnings.append('Modification date changed from ' + stat_old[STAT_MOD_DATE] +
                            ' to ' + stat_new[STAT_MOD_DATE] + ' of ' + path)

    def execute(self):
        self.init_verification_dict()

        for root, dirs, files in os.walk(self.monitor):
            self.no_of_dirs += 1
            self.no_of_files += len(files)

            if root in self.verification_dict:
                self.stat_check(root)
                for f in files:
                    if f in self.verification_dict[root][FILE_KEY]:
                        self.stat_check(root, f)
                        del self.verification_dict[root][FILE_KEY][f]
                    else:
                        warnings.append('New file ' + f + ' added in ' + root)
                for key, value in self.verification_dict[root][FILE_KEY].iteritems():
                    warnings.append('File ' + key + ' deleted from ' + root)
                del self.verification_dict[root]
            else:
                warnings.append('New directory added ' + root)
                for f in files:
                    warnings.append('New file ' + f + ' added in ' + root)

        for key, value in self.verification_dict.iteritems():
            warnings.append('Directory ' + key + ' is deleted')

        self.generate_report()

    def generate_report(self):
        with open(self.report, 'w+') as f:
            f.write(monitor_name + ': ' + self.monitor + '\n' +
                    verification_name + ': ' + self.verification + '\n' +
                    report_name + ': ' + self.report + '\n' +
                    'Directories: ' + str(self.no_of_dirs) + '\n' +
                    'Files: ' + str(self.no_of_files) + '\n' +
                    'Number of warnings: ' + str(len(warnings)) + '\n' +
                    'Execution time: ' + str(round(time.time() - self.start_time, 5)) + ' seconds' + '\n\n' +
                    '\n'.join(warnings)
                    )
