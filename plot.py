from operator import itemgetter

import click
import csv
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime

import constants


def parse_row(row):
    return datetime.fromisoformat(row[0]), *map(int, row[1:])


@click.command()
@click.argument("file", type=click.File(mode="r"))
def main(file):
    reader = csv.reader(file)
    head = next(reader)
    rows = sorted(set(map(parse_row, reader)))

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

    fig.legend(labs, loc="outside right upper")

    plt.show()


if __name__ == "__main__":
    main()
