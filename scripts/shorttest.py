import os
import subprocess
import sys

if hasattr(sys, "frozen"):
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    os.chdir(os.path.dirname(__file__))
    os.chdir("..")
    approot = os.path.abspath(os.curdir)

smartctl = os.path.join(approot, 'smartmontools', 'bin', 'smartctl.exe')
output = subprocess.Popen([smartctl, '-l', 'selftest', 'C:\\'], stdout=subprocess.PIPE).communicate()[0].split('\n')
print "\n".join(output[5:])
result = 'Passed' if any('Completed without error' in i for i in output) else 'Failed'
with open(os.path.join(approot, 'logs', 'short_test_result.txt'), 'a') as file:
    file.write('{}\t{}'.format(os.environ['COMPUTERNAME'], result))
