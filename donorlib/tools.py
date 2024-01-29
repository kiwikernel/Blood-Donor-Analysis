from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import time
import requests
from donorlib import const as c
import geopandas as gpd


def pullcsv(csvlist = c.csvlist):
    download = c.download
    for csv in csvlist:
        time.sleep(0.5)
        csvfile = pd.read_csv(f"{csv}")
        csvname = csv.split("/")[-1].split(".")[0]
        csvfile.to_csv(f"{download}{csvname}.csv",index=False)

def pullparquet(parquet = c.donor_retention_url):
    download = c.download
    file = pd.read_parquet(f"{parquet}",engine="pyarrow")
    filename = parquet.split("/")[-1].split(".")[0]
    file.to_parquet(f"{download}{filename}.parquet",engine="pyarrow")

def send_telegram(chat_id = c.chat_id,token = c.token, text = None, photo = None):
    # telegram api for sending messages
    api_url = f'https://api.telegram.org/bot{token}/sendMessage'

    # prepping data to be sent
    data = {'chat_id': chat_id}
    files = None

    if text:
        data['text'] = text

    if photo:
        # telegram api for sending photos
        api_url = f"https://api.telegram.org/bot{token}/sendPhoto"

        # open photo file
        with open(photo,'rb') as photo_file:
            # prepping photo to be sent
            files = {'photo': photo_file.read()}
            if text:
                # Adding caption to photo is present
                data['caption'] = text

    # Disable SSL certificate verification
    requests.packages.urllib3.disable_warnings()
    
    # sending the message/photo
    response = requests.get(api_url, data=data, files=files, verify=False)

    # returning response if unsuccessful
    if response.status_code != 200: 
        print(f'Failed to send message/photo. Status code: {response.status_code}, Response: {response.text}')

    time.sleep(0.5)

def Readcsv(filename):
    data_loc = c.download
    df1 = pd.read_csv(f"{data_loc}{filename}.csv")
    return df1
 
def Readparquet(filename):
    data_loc = c.download
    df1 = pd.read_parquet(f"{data_loc}{filename}.parquet",engine="pyarrow")
    return df1

def retention_viz():
    # read dataset
    df = Readparquet("blood_donation_retention_2024")

    # set visit_date as datetime format
    df['visit_date'] = pd.to_datetime(df['visit_date'])

    # remove donors above 65 years old
    y65 = datetime.now().year - 65

    # remove donors below 18 years old
    y18 = datetime.now().year - 18

    # select data for the past 5 years
    y5 = datetime.now() - timedelta(days=365*5)
    query = f"birth_date >= {y65} & visit_date >= '{y5}' & birth_date < {y18}"
    df = df.query(query)

    # preparing data for visualization
    donor_summary = pd.DataFrame()
    donor_summary["first_donation"] = df.groupby("donor_id")["visit_date"].min()
    donor_summary["last_donation"] = df.groupby("donor_id")["visit_date"].max()
    donor_summary["days_of_donation"] = donor_summary["last_donation"] - donor_summary["first_donation"]
    donor_summary["donation_count"] = df.groupby("donor_id")["visit_date"].count()
    donor_summary["birth_year"] = df.groupby("donor_id")["birth_date"].first()
    donor_summary["donor_age"] = datetime.now().year - donor_summary["birth_year"]
    
    # to produce visualization
    y1 = donor_summary["donation_count"]
    y2 = donor_summary.query("donation_count > 1")["donation_count"].median()
    x = donor_summary["donor_age"]
    fig, ax = plt.subplots()
    ax.scatter(x, y1, color="red", alpha=.7, s=5)
    ax.axhline(y=y2, color='blue', linestyle='--')
    ax.set_title(f'Donation Count vs Donor Age Since Year {y5.year}\n(Horizontal line: median retuning donors)')
    ax.set_xlabel('Donor Age')
    ax.set_ylabel('Donation Count')
    ax.grid(False)

    # to save the visualization
    plt.savefig(f"{c.dataviz}donor_retention.png",bbox_inches="tight")

def nationaltrend_viz():
    # reading datasets and extracting required columns
    df1 = Readcsv("newdonors_state")[["date","state","total"]]
    df2 = Readcsv("donations_state")[["date","state","daily"]]

    # setting date columns as datetime format
    df1["date"] = pd.to_datetime(df1["date"])
    df2["date"] = pd.to_datetime(df2["date"])

    # renaming columns
    df1.rename(columns={"total":"new donors"},inplace=True)
    df2.rename(columns={"daily":"total donors"},inplace=True)

    #merging both dataframes
    df_merged = pd.merge(df2, df1, on=['state', 'date'], how='inner')  
    
    # creating new columns in merged dataframe
    df_merged["returning donors"] = df_merged["total donors"] - df_merged["new donors"]

    # aggregating data into weekly bins to reduce noise effect
    def custom_agg(series):
        return series.iloc[0] if series.dtype == 'object' else series.sum()
    
    df = df_merged.groupby("state",as_index=False).resample("W-Mon", on="date").agg(custom_agg).reset_index()
    
    # selecting data for past 3 months
    date = datetime.now() - timedelta(days=30.5*3)

    # select Malaysia data for national representation
    state = "Malaysia"
    query = f"state =='{state}' & date >= '{date}'"
    df = df.query(query)

    # Calculate the difference between target date and current date
    def date_to_week_delta(target_date):
        delta = target_date - datetime.now()
        
        # Convert the time difference to weeks
        week_delta = delta.days / 7
        return week_delta
    
    df["week_delta"] = df["date"].apply(date_to_week_delta).astype("int")

    # creating axes labels
    df["xlabel"] = df["date"].astype("str") + ' (' + df["week_delta"].astype("str") +')'

    # preparing data for visualization
    x = df['xlabel']
    y1 = df['new donors']
    y2 = df['total donors']
    
    # producing the visualization
    fig, ax = plt.subplots()
    ax.bar(x,y2/1000,label='Returning Donors',color='blue',alpha=.9)
    ax.bar(x,y1/1000,label='New Donors',color='red',alpha=.9)
    ax.set_title('National Weekly Blood Donations for Last 3 Months')
    ax.set_ylabel('No. of Blood Donors (x1,000)')
    ax.set_xlabel('Week (Delta)')
    ax.legend()
    plt.xticks(rotation=80)

    
    # to save the visualization
    plt.savefig(f"{c.dataviz}national_donor_trend.png",bbox_inches="tight")

def statetrend_viz():
    # reading datasets and extracting required columns
    df1 = Readcsv("newdonors_state")[["date","state","total"]]
    df2 = Readcsv("donations_state")[["date","state","daily"]]

    # setting date columns as datetime format
    df1["date"] = pd.to_datetime(df1["date"])
    df2["date"] = pd.to_datetime(df2["date"])

    # renaming columns
    df1.rename(columns={"total":"new donors"},inplace=True)
    df2.rename(columns={"daily":"total donors"},inplace=True)

    #merging both dataframes
    df_merged = pd.merge(df2, df1, on=['state', 'date'], how='inner')  
    
    # creating new columns in merged dataframe
    df_merged["returning donors"] = df_merged["total donors"] - df_merged["new donors"]
    
    # selecting data for past 3 months
    date = datetime.now() - timedelta(days=30.5*3)

    # select Malaysia data for national representation
    state = "Malaysia"
    query = f"state !='{state}' & date >= '{date}'"
    df = df_merged.query(query)

    # aggregating data by states
    def custom_agg(series):
        return series.iloc[0] if series.dtype == 'object' else series.sum()
    
    df = df[["state","total donors","new donors"]].groupby("state",as_index=False).agg(custom_agg).sort_values("total donors",ascending=False)

    # preparing data for visualization
    x = df['state']
    y1 = df['new donors']
    y2 = df['total donors']

    # producing the visualization
    fig, ax1 = plt.subplots()
    ax1.bar(x,y2/1000,label='Returning Donors',color='blue',alpha=.9)
    ax1.bar(x,y1/1000,label='New Donors',color='red',alpha=.9)
    ax1.set_title('Blood Donations by State for Last 3 Months')
    ax1.set_ylabel('No. of Blood Donors (x1,000)')
    ax1.set_xlabel('State')
    ax1.legend()
    plt.xticks(rotation=80)
        
    # to save the visualization
    # plt.tight_layout()
    plt.savefig(f"{c.dataviz}state_donor_trend.png",bbox_inches="tight")

def donormap_viz():
    # reading datasets and extracting required columns
    df = Readcsv("donations_state")[["date","state","daily"]]

    # setting date columns as datetime format
    df["date"] = pd.to_datetime(df["date"])

    # renaming columns
    df.rename(columns={"daily":"total donors"},inplace=True)

    # selecting data for past 7 days
    date = datetime.now() - timedelta(days=7)

    # select Malaysia data for national representation
    state = "Malaysia"
    query = f"state !='{state}' & date >= '{date}'"
    df = df.query(query)

    # aggregating data by states
    def custom_agg(series):
        return series.iloc[0] if series.dtype == 'object' else series.sum()
    
    df = df[["state","total donors"]].groupby("state",as_index=False).agg(custom_agg).sort_values("total donors",ascending=False)

    # Load the shapefile containing Malaysia's states
    malaysia_states = gpd.read_file(".\shapefile\malaysia\malaysianStates.shp")
    malaysia_states.at[12,"name"] = "Terengganu"

    # merging shapefile table with the dataframe
    malaysia_states = pd.merge(malaysia_states, df, left_on='name', right_on='state', how='inner')

    # calculate legend range
    cut = .2
    up_limit = malaysia_states["total donors"].quantile(1-cut)
    lo_limit = malaysia_states["total donors"].quantile(cut)

    # Plot the geographic heatmap
    fig, ax = plt.subplots(figsize=(8,4))
    malaysia_states.plot(column = "total donors", cmap='plasma', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, vmin=lo_limit, vmax=up_limit)

    # Add title and labels
    plt.title('Geographic Heatmap of Blood Donations in Past 7 Days')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # save the visualization    
    plt.savefig(f"{c.dataviz}donor_map.png",bbox_inches="tight")
