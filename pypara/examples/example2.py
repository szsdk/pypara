# run by
# pypara -p example2.py --run "echo {f}" --count 3

import click


@click.command()
@click.option("--count", "-c", type=int)
def generator(count):
    return range(count)
