import json
import boto3
import pandas
import argparse
import sys
import os.path

#1.Preparing and parsing additional arguments.
parser = argparse.ArgumentParser()

parser.add_argument('--col',nargs = '+', action = 'store', dest = 'cols', default = [], help = "List of columns to print")
parser.add_argument('--sort',action = 'store', dest = 'sort', default = '', help = "Sorting value")


results = parser.parse_args()

cols = results.cols
sort = results.sort

#2.Checking if file exist and reading config data from file.
if os.path.isfile('config.json'):
    config_file = open('config.json')
else:
    print("config.json file is recquired! Please provide it.")
    sys.exit()

config_data = json.load(config_file)

#3.Accessing AWS S3 bucket.
client = boto3.client(
    's3',
    aws_access_key_id = config_data['aws_access_key_id'],
    aws_secret_access_key = config_data['aws_secret_access_key'],
)
obj = client.get_object(
    Bucket = config_data['bucket'],
    Key = config_data['object'],
)

#4.Reading data from file.
data=pandas.read_csv(obj['Body'])

#5.Veryfying if values in --col provided by user are correct.
headers = data.columns

for col in cols:
    if col not in headers:
        print("This header does not exist. Existing header: "
              + ' '.join(headers)
              + " Please for --cols type in only existing headers.")
        sys.exit()

#6.Picking only provided columns (in case columns are provided)
if cols:
    data = data[cols]

#7.Veryfying if result should be sorted and if sorting value is correcct.
if sort and (sort in cols or (not cols and sort in headers)):
    data = data.sort_values(by=sort)
elif sort:
    print("Sorting value is not in columns value.")
    sys.exit()

#8.Printing result.
if __name__ == "__main__":
    print(data)