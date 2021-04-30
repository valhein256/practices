#!/usr/bin/python3
import datetime

info_log_path = "/var/log/app/info.log"

with open(info_log_path, "a") as f:
    date = datetime.datetime.now()
    f.write("{}, {}".format(str(date), "Hello\n"))
