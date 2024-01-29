from donorlib import tools as t
import time
from datetime import datetime, timedelta
import logging as logger
from donorlib import const as c
import schedule as sch

logger.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def Main_task(): 
    t.pullcsv()
    logger.info('Pulling CSV completed')
    time.sleep(1)

    t.pullparquet()
    logger.info('Pulling Parquet completed')
    time.sleep(1)

    t.nationaltrend_viz()
    logger.info('National blood donation trend completed')
    time.sleep(1)

    t.statetrend_viz()
    logger.info('State blood donation trend completed')
    time.sleep(1)

    t.retention_viz()
    logger.info('Blood donor retention completed')
    time.sleep(1)

    t.donormap_viz()
    logger.info('Blood donation heatmap completed')
    time.sleep(1)
    
    t.send_telegram(text=f"Daily Blood Donation Update\n{datetime.now().strftime(c.time_string)}", photo=None)
    
    for text, photo in zip(c.Text, c.Photo):
        try: t.send_telegram(text=f"{text}", photo=f"{c.dataviz}{photo}")
        except Exception as e: logger.info(e)

    logger.info('Messages sent')
    time.sleep(1)

try: 
    logger.info('Script started')
    
    # initial run of the task
    Main_task()

    # scheduling the task to run everyday at 10:00 AM and 5:00 PM
    sch.every().day.at("10:00").do(Main_task)
    sch.every().day.at("17:00").do(Main_task)
    
    # control variable to end the task after 1 year (365 days)
    end_date = datetime.now() + timedelta(days=365)
    exit_flag = False
    
    # the task will run as schduled until control variable is True
    while not exit_flag:
        sch.run_pending()
        time.sleep(30)

        if datetime.now() > end_date:
            exit_flag = True
        
except Exception as e: 
    logger.info('Script encountered error')
    logger.info(e)

finally:
    logger.info('Script ended\n')
