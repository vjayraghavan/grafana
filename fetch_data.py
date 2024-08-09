import argparse
import requests
import os
import pandas as pd
import datetime
# uid= 'edsob1tq38zcwf'
username = 'admin'
password = 'admin'

# date_from = '2024-07-24T13:25:00'
# date_to = '2024-07-24T15:45:00'
# os.environ['DATASOURCE'] = 'prometheus'
# os.environ['UID'] = 'edsob1tq38zcwf'

parser = argparse.ArgumentParser()
parser.add_argument('-DS', '--datasource',  default=None)
parser.add_argument('-DF', '--date_from',  default=None)
# parser.add_argument('-DT', '--date_to',  default=None)
parser.add_argument('--uid',         default=None)
parser.add_argument('--query_name',  help='expr,rawsql', default='expr')
parser.add_argument('--query',         required=True, help='prometheus_http_response_size_bytes_count')
args = parser.parse_args()

datasource = args.datasource or os.environ.get('DATASOURCE')
date_from = args.date_from or os.environ.get('DATE_FROM')
# date_to = args.date_to or os.environ.get('DATE_TO')
uid = args.uid or os.environ.get('UID')
query_name = args.query_name
query = args.query


def convert_timestamp_to_epoch(val):
    return int(datetime.datetime.strptime(val, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc).timestamp()) * 1000

def convert_to_mapped_type(val, type):
    if type=='time':
        return [datetime.datetime.utcfromtimestamp(i/1000) for i in val]
    return val

def main():
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = f'http://{username}:{password}@localhost:3000/api/ds/query'


    params ={
        "queries": [
            {"datasource":{"type": datasource, "uid": uid},
                        'format': 'table', 
                        query_name: query}
                        ],
            "from": str(date_from),
            "to": 'now'
    }

    response = requests.post(url, json = params, headers=headers)
    data = response.json()

    for fidx, frame in enumerate(data['results']['A']['frames']):

        fields = frame['schema']['fields']
        values =  frame['data']['values']
        if not values:
            print('DATA RETRIEVED IS EMPTY')
            return
        label = f'{fidx}_frame_data'
        if len(fields) > 1:
            fname = fields[1].get('labels', {}).get('__name__', '')
            handler_name = fields[1].get('labels', {}).get('handler', '').replace('/','_')
            label = f'{fname}{handler_name}' or label

        
        # label = f"{fields[1]['labels']['__name__']}{fields[1]['labels']['handler'].replace('/','_')}"


        data_dict = {fields[idx]['name']:convert_to_mapped_type(val, fields[idx]['type']) for idx, val in enumerate(values)}
        df = pd.DataFrame(data_dict)
        df.to_csv(f'{label}.csv', index = False)
    print('SAVED TO CSV')

main()

# python fetch_data.py --query prometheus_http_response_size_bytes_count --datasource prometheus --uid edsob1tq38zcwf --date_from 2024-07-24T13:25:00 --date_to 2024-07-24T15:45:00
