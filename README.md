Script that works to clear up issues relating to .csv files exported from Twitter.

In some cases, the metrics are broken due to the raw text being lifted from each tweet, resulting in multi-line .csv files.

This program will accept such broken files and return them to corrected .csv files, then convert to .xlsx format.

Usage:
$ python csv_converter.py -CSV twitter_output.csv

Note: Will not work with python2.7