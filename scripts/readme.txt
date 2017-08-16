check.py : analyze S.M.A.R.T attributes to predict disk failures
parse_logs.py:
    --list : creates list of computers
    --error=filename : parses failed hosts from the file in logs directory
shorttest.py: analyze 'short_test' results

to build use:
pyinstaller 'script name' --onefile --distpath="../" --clean --noconfirm --workpath="../temp" --specpath="../temp"

to deploy use:
\\mtcdc1\netlogon\Script\PSTBackup\PSTCopy\PSTools\PsExec.exe @\\mtcntserver\sysvol\apps\IT\smartctl\scripts\users_list.txt -u mtcdomain\superman -n 5 \\mtcntserver\sysvol\apps\IT\smartctl\check.exe

to start test on failed computers use:
\\mtcdc1\netlogon\Script\PSTBackup\PSTCopy\PSTools\PsExec.exe @\\mtcntserver\sysvol\apps\IT\smartctl\scripts\hosts_failed_CN.txt -u mtcdomain\superman -n 5 \\mtcntserver\sysvol\apps\IT\\smartctl\smartmontools\bin\smartctl.exe --test=short C:\

to check results use:
\\mtcdc1\netlogon\Script\PSTBackup\PSTCopy\PSTools\PsExec.exe @\\mtcntserver\sysvol\apps\IT\smartctl\scripts\hosts_failed_CN.txt -u mtcdomain\superman -n 5 \\mtcntserver\sysvol\apps\IT\smartctl\shorttest.exe