# check.py : analyze S.M.A.R.T attributes to predict disk failures

## parse_logs.py:
    --list : creates list of computers
    --error=filename : parses failed hosts from the file in logs directory
shorttest.py: analyze 'short_test' results

## to build use:
pyinstaller 'script name' --onefile --distpath="../" --clean --noconfirm --workpath="../temp" --specpath="../temp"