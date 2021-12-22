# SG Stocks Financial Reports

Getting Financial report data listed on https://investors.sgx.com into a pandas dataframe

## Install python libraries

This works on python 3.9.7

### Using Anaconda

`conda config --add channels conda-forge`

`conda config --add channels microsoft`

`conda install --file requirements.txt`

### Install browser binaries

`playwright install`

## Run script

`python run.py`

It prints out of the following dataframes in this order:

1. Income Statement
2. Balance Sheet
3. Cash Flows
