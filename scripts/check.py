import os
import subprocess
import sys


class smartctl:
    def __init__(self, error_hunt, approot):
        self.error_hunt = error_hunt
        self.approot = approot
        self.smartctl_path = os.path.join(self.approot, 'smartmontools', 'bin', 'smartctl.exe')
        self.columns = ['ID', 'ATTRIBUTE_NAME', 'FLAG', 'VALUE', 'WORST', 'THRESH', 'TYPE', 'UPDATED',
                        'WHEN_FAILED', 'RAW_VALUE']

    def check_drives(self):
        output = subprocess.Popen([self.smartctl_path, '-l', 'error', 'c:\\'], stdout=subprocess.PIPE).communicate()[0]
        if 'Read Device Identity failed: Input/output error'.lower() in output.lower():
            self.__log__('hosts_unsupported.txt', '{}\n'.format(os.environ['COMPUTERNAME']))
            return 'Disk Unsupported'
        else:
            return self.__analyze__()

    def __analyze__(self):
        output = subprocess.Popen([self.smartctl_path, '-a', 'c:\\'], stdout=subprocess.PIPE).communicate()[0].split(
            '\n')
        log = []
        fail_count = 0
        for index, lines in enumerate(output):
            if any(i.lower() in lines.lower() for i in self.error_hunt):
                row = dict(zip(self.columns, filter(None, lines.strip().split(' '))))
                if self.__safe_cast__(row['RAW_VALUE']) > 0:
                    log.append(lines)
                    fail_count += 1
        if fail_count == 0:
            self.__log__('hosts_passed.txt', os.environ['COMPUTERNAME'] + '\n')
            return 'Disk Passed'
        else:
            self.__log__('hosts_failed.txt', '{}\n{}'.format(os.environ['COMPUTERNAME'], '\n'.join(log)))
            return 'Disk Failed the test \nAttributes: \n' + '\n'.join(log)

    def __log__(self, file_name, data):
        with open(os.path.join(self.approot, 'logs', file_name), 'a') as file:
            file.write(data)

    def __safe_cast__(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0


if hasattr(sys, "frozen"):
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    os.chdir(os.path.dirname(__file__))
    os.chdir("..")
    approot = os.path.abspath(os.curdir)
errors = ['Reallocated_Sector_Ct', 'Reallocated_Event_Ct', 'Spin_Retry_Count', 'Runtime_Bad_Block', 'End-to-End_Error',
          'Current_Pending_Sector', 'Offline_Uncorrectable', 'Soft_Read_Error_Rate', 'TA_Counter_Detected',
          'Reported_Uncorrectable_Errors', ]
print smartctl(errors, approot).check_drives()
