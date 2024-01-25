import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from donorlib import const as c

def pullcsv(csvlist = c.csvlist):
    download = c.download
    print(download)
    for csv in csvlist:
        print(csv)
        csvfile = pd.read_csv(f"{csv}")
        csvname = csv.split("/")[-1].split(".")[0]
        print(csvname)
        csvfile.to_csv(f"{download}{csvname}.csv",index=False)

def pullparquet():
    pass

def send2group():
    pass