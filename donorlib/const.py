

# telegram group
token = '6754519975:AAEipis4kLVurvzATUP49IxrfCH6MQ35Rkw'
bot_id = '@kiwikernelbot'
chat_id = -1002068798727
time_string = '%a %d-%b-%Y %H:%M:%S'
Text = ["National Weekly Trend for Last 3 Months", "State Trend for Last 3 Months", "Individual Max Donations by Age for Last 5 Years", "Geographic Heatmap of Donations in Past 7 Days"]
Photo = ["national_donor_trend.png", "state_donor_trend.png", "donor_retention.png", "donor_map.png"]

# download location and files
download = "./downloads/"
donor_retention_url = "https://storage.data.gov.my/healthcare/blood_donation_retention_2024.parquet"
donor_facilities_url = 'https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_facility.csv'
donor_state_url = 'https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_state.csv'
newdonor_facilities_url = 'https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_facility.csv'
newdonor_state_url = 'https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_state.csv'
csvlist = [donor_facilities_url,donor_state_url,newdonor_facilities_url,newdonor_state_url]

# location to save visualization
dataviz = "./dataviz/"