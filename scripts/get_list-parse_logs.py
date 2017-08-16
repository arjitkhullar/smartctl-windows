import os
import re
import sys

from ldap3 import Server, Connection

conn = Connection(Server('mtcdom.multimatic.com', get_info='NO_INFO'), 'lnxupdates@mtcdom.multimatic.com',
                  '85multimtc', auto_bind=True)
entry = conn.search('DC=mtcdom,DC=multimatic,DC=com',
                    '(objectclass=Computer)', attributes=["CN", "operatingSystem", "description"])


def get_list():
    log('pc_list.txt', "\n".join(filter(None, [
        (lambda x: '' if (x == '[]') else x)(str(i['cn'])) if 'Windows 7 Professional' in i['operatingSystem'] else None
        for i in conn.entries])))


def get_failed_computers_description(file_name):
    failed_list = []
    with open(os.path.join(os.path.abspath(os.curdir), 'logs', file_name), 'r') as passed:
        for i in passed.readlines():
            match = re.search('(\w+-\w+-\w+)', i.strip(), re.IGNORECASE)
            if match: failed_list.append(match.group(1))
    log('hosts_failed_info.txt', "\n".join(filter(None, ['{}\t{}'.format(str(i['CN']), str(i['description']))
                                                         if any(j in str(i['cn']) for j in failed_list)
                                                         else None for i in conn.entries])))
    log('hosts_failed_CN.txt', "\n".join(filter(None, [str(i['CN']) if any(j in str(i['cn']) for j in failed_list)
                                                       else None for i in conn.entries])))


def log(file, data):
    print 'created ' + file + '.txt'
    with open(os.path.join(os.path.abspath(os.curdir), 'logs', file), 'w') as out:
        out.write(data)


if hasattr(sys, "frozen"):
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    os.chdir("..")

if re.search('\D+list|list', " ".join(sys.argv[1:])):
    get_list()
elif re.search('\D+error|error', " ".join(sys.argv[1:])):
    file_match = re.search('(?:=)(.+.txt)', " ".join(sys.argv[1:]))
    if file_match:
        if os.path.exists(os.path.join(os.path.abspath(os.curdir), 'logs', file_match.group(1).strip())):
            get_failed_computers_description(file_match.group(1).strip())
        else:
            print 'File Doesn\'t Exist'
    else:
        print 'Invalid file name'
else:
    print 'Invalid Arguments\tUsage:\n --list : creates list of computers \t--error=filename : parses failed hosts from the file in logs directory'
