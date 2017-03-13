import os
import time

from helper import monitor_name, verification_name, FILE_KEY, DIR_KEY, collect_info


def exec_initialization(monitor, verification, report):
    start_time = time.time()
    verification_dict = {}
    no_of_dirs, no_of_files = 0, 0
    for root, dirs, files in os.walk(monitor):
        no_of_dirs += 1
        no_of_files += len(files)

        verification_dict[root] = {}
        verification_dict[root][DIR_KEY] = collect_info(root)
        file_dict = verification_dict[root][FILE_KEY] = {}
        for file_name in files:
            file_dict[file_name] = collect_info(root + '/' + file_name)

    with open(verification, 'w+') as f:
        f.write(str(verification_dict))

    with open(report, 'w+') as f:
        f.write(monitor_name + ': ' + monitor + '\n' +
                verification_name + ': ' + verification + '\n' +
                'Directories: ' + str(no_of_dirs) + '\n' +
                'Files: ' + str(no_of_files) + '\n' +
                'Execution time: ' + str(round(time.time() - start_time, 5)) + ' seconds')
