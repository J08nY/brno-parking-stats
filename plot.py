from operator import itemgetter

import click
import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import constants


def parse_row(row):
    return datetime.fromisoformat(row[0]), *map(int, row[1:])


@click.command()
@click.argument("file", type=click.File(mode="r"))
def main(file):
    reader = csv.reader(file)
    head = next(reader)
    # Load
    rows = list(map(parse_row, reader))

    # Fix borked time
    for i in range(len(rows) - 1):
        td = rows[i + 1][0] - rows[i][0]
        if td < timedelta():
            rows[i] = (rows[i][0] - timedelta(days=1), *rows[i][1:])

    # Deduplicate
    rows = sorted(set(rows))

    # XXX Messy piece of terrible matplotlib follows XXX

    fig, axs = plt.subplots(1, 2, layout="constrained")

    ax = axs[0]
    ax.set_xlabel("Time")
    ax.set_ylabel("Free")

    labs = []
    for i, id in enumerate(head[1:]):
        ax.step(list(map(itemgetter(0), rows)), list(map(itemgetter(i + 1), rows)), label=constants.pd_names[id])
        labs.append(constants.pd_names[id])

    ax = axs[1]
    ax.set_xlabel("Time")
    ax.set_ylabel("Taken")

    for i, id in enumerate(head[1:]):
        ax.step(list(map(itemgetter(0), rows)), list(map(lambda x: constants.pd_caps[id] - x[i + 1], rows)),
                label=constants.pd_names[id])

    ylim_1 = max(axs[0].get_ylim()[1], axs[1].get_ylim()[1])
    axs[0].set_ylim((0, ylim_1))
    axs[1].set_ylim((0, ylim_1))

    fig.legend(labs, loc="outside right upper")

    plt.show()


if __name__ == "__main__":
    main()
