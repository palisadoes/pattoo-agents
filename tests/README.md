# Tests

Welcome to the developer testing section of `pattoo-agents`.

## Running unittests

You can run all the unittests in this directory by executing the `_do_all_tests.py` script.

## Duplicate Error Logging Codes
`pattoo-agents` tries to make it easy for developers and users to see where there are issues in the code, operating conditions or configuration by generously logging events.

The codes should be unique to make it easier to find the source of an issue.

If you are a developer, you can search to see whether the logging error codes you have selected for your work have duplicates by running the `error_code_report.py` script in this directory. It will give you an output like this.

```bash
$ ./error_code_report.py
Pattoo Error Code Summary Report
--------------------------------
Starting Code              : 1001
Ending Code                : 1569
Duplicate Codes to Resolve : [1029, 1186]
Available Codes            : [1007, 1008, 1010, 1011, 1012]
$
```
Use `grep` or some other similar utility to determine the duplication location and then correct it.