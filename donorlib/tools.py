import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from donorlib import const as c

time_epoch = time.time()

def pullcsv(csvlist = c.csvlist):
    download = c.download
    for csv in csvlist:
        csvfile = pd.read_csv(f"{csv}")
        csvname = csv.split("/")[-1].split(".")[0]
        csvfile.to_csv(f"{download}{csvname}.csv",index=False)

def pullparquet(parquet = c.donor_retention_url):
    download = c.download
    file = pd.read_parquet(f"{parquet}",engine="pyarrow")
    filename = parquet.split("/")[-1].split(".")[0]
    file.to_parquet(f"{download}{filename}.parquet",engine="pyarrow")

def send2group(chat_id = c.chat_id,token = c.token, message = c.sample_msg):
    local_time = time.ctime(time_epoch)
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {'chat_id': chat_id, 'text': f"{message} {local_time}"}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')