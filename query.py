from operator import itemgetter

from datetime import datetime
import csv
import requests
import click

import constants


@click.command()
@click.argument("file", type=click.File(mode="a+"))
def main(file):
    resp = requests.get(constants.pd_url, headers={"User-Agent": "brno-parking-stats/0.0.1"})
    data = resp.json()
    times = set(map(itemgetter("statusTime"), data.values()))
    if len(times) > 1:
        # This happens sometimes, but to have nice data format I don't see a better solution rn.
        raise ValueError("Oops")
    time = datetime.strptime(times.pop(), "%H:%M")
    timestamp = datetime.now().replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)

    writer = csv.writer(file)

    # This is a bit of a mess to handle both a real file and stdout.
    end = 0
    try:
        end = file.tell()
        file.seek(0)
        reader = csv.reader(file)
        next(reader)
        file.seek(end)
    except:
        if end != 0:
            file.seek(end)
        writer.writerow(("timestamp", *constants.pd_names.keys()))

    pd_data = (data[id]["free"] for id in constants.pd_names)
    writer.writerow((timestamp, *pd_data))


if __name__ == "__main__":
    main()
