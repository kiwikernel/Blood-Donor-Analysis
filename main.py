from donorlib import tools as t
import time
from datetime import datetime, timedelta
import logging
from donorlib import const as c
import schedule as sch

logging.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def Main_task(): 
    t.pullcsv()
    logging.info('Pulling CSV completed')
    time.sleep(1)

    t.pullparquet()
    logging.info('Pulling Parquet completed')
    time.sleep(1)

    t.nationaltrend_viz()
    logging.info('National blood donation trend completed')
    time.sleep(1)

    t.statetrend_viz()
    logging.info('State blood donation trend completed')
    time.sleep(1)

    t.retention_viz()
    logging.info('Blood donor retention completed')
    time.sleep(1)

    t.donormap_viz()
    logging.info('Blood donation heatmap completed')
    time.sleep(1)
    
    t.send_telegram(text=f"Blood Donation Update\n{datetime.now().strftime(c.time_string)}", photo=None)
    
    for text, photo in zip(c.Text, c.Photo):
        try: t.send_telegram(text=f"{text}", photo=f"{c.dataviz}{photo}")
        except Exception as e: logging.info(e)

    logging.info('Messages sent')
    time.sleep(1)

try: 
    logging.info('Script started')
    
    # initial run of the task
    Main_task()

    # scheduling the task to run everyday on the following times
    sch.every().day.at("11:00").do(Main_task)
    sch.every().day.at("20:00").do(Main_task)
    
    # control variable to end the task after 365 days (1 year)
    end_date = datetime.now() + timedelta(days=365)
    exit_flag = False
    
    # the task will run as schduled until control variable is True
    while not exit_flag:
        sch.run_pending()
        time.sleep(30)

        if datetime.now() > end_date:
            exit_flag = True
        
except Exception as e: 
    logging.info('Script encountered error')
    logging.info(e)

finally:
    logging.info('Script ended\n')
