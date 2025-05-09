import os
import time
import glob
import logging
from datetime import datetime

cand_plot_dir = "/hdd/data/candidates/T3/candplots/"
target_service = "cand_plotter.service"
logfile = "/home/user/grex/t3/GReX-T3/services/monitor_candidate.log"
check_interval=60
start_timing = 11 # Hour! 
end_timing = 13 # Hour!

logging.basicConfig(filename=logfile,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("Starting candidate monitor service")

last_seen = set(glob.glob(os.path.join(cand_plot_dir, "*")))
new_file_detected = False
already_restarted_today = False
today_date = datetime.now().date()

while True:
    now = datetime.now()

    # Reset daily flags at midnight
    if now.date() != today_date:
        today_date = now.date()
        already_restarted_today = False
        new_file_detected = False
        last_seen = set(glob.glob(os.path.join(cand_plot_dir, "*")))
        logging.info("Midnight reset for daily tracking.")

    # Monitor between start_timing and end_timing e.g. 11:00 ~ 13:00
    if start_timing <= now.hour < end_timing and not already_restarted_today:
        current_files = set(glob.glob(os.path.join(cand_plot_dir, "*")))
        new_files = current_files - last_seen

        if new_files:
            logging.info(f"Detected new candidate files: {new_files}")
            time.sleep(check_interval*2)
            logging.info(f"Restarting service after the new candidate plotting complete: {target_service}")
            os.system(f"sudo systemctl restart {target_service}")
            already_restarted_today = True
            new_file_detected = True
            last_seen = current_files
        else:
            logging.info("Monitoring, no new files yet. Waiting for a new candidate.")

    # If no new file, restart at exactly 13:00
    elif now.hour == end_timing and now.minute <= 2 and not already_restarted_today:
        logging.info(f"No new files detected before {end_timing}:00. Restarting service anyway.")
        os.system(f"sudo systemctl restart {target_service}")
        already_restarted_today = True

    time.sleep(check_interval)
