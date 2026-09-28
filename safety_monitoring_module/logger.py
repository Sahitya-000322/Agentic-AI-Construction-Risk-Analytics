import csv
from datetime import datetime

def save_log(status):
    with open("logs/violations.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), status])

