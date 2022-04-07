#!/usr/bin/env python3
from importlib.machinery import SourceFileLoader
import os
import sys
import multiprocessing as mp
import click
from click_default_group import DefaultGroup
from inspect import signature
import itertools as it
import more_itertools as mi
from pathlib import Path

sys.dont_write_bytecode = True


def load_from_file(filepath: Path):
    if filepath.suffix.lower() == ".py":
        return SourceFileLoader(filepath.stem, str(filepath)).load_module()
    else:
        raise Exception(f"can not load {filepath}")


class RunCmd:
    def __init__(self, cmd):
        self.cmd = cmd
        self.__doc__ = f"run shell command: {cmd}"

    def __call__(self, f):
        os.system(self.cmd.format(f=f))


def get_default_generator(input, splitby):
    if input != "-":
        ans = {}
        exec(f"__ans = {input}", {}, ans)
        return ans["__ans"]

    input = it.chain.from_iterable(sys.stdin)

    def wrap():
        for x in mi.split_at(input, lambda x: x in splitby):
            x = "".join(x).strip()
            if len(x) > 0:
                yield x

    return wrap()


@click.group(cls=DefaultGroup, default='main', default_if_no_args=True)
def cli():
    pass


@cli.command(
    context_settings={"ignore_unknown_options": True},
    help="""Example:

`pypara -g "range(10)" -r "echo {f}"`

\b
With pipe
`echo "0 1 2" | pypara --run "echo cmd{f}"`

\b
Change spliting character
`echo "0\\n1\\n2" | pypara  --run "echo cmd{f}" --splitby $'\\n'`

\b
`pypara -p example1.py`

\b
use ruuning function from example1.py with given generator
`pypara -p example1.py -g "1 2 3"`

\b
use generator from example1.py with given running command
`pypara -p example1.py -r "echo cmd{f}"`

\b
Pass argument to generator in example2.py
`pypara -p example2.py --run "echo cmd{f}" --count 3`
""",
)
@click.option(
    "--pkg",
    "-p",
    default=None,
    type=Path,
    help="path to a python file, which usually includes a variable/function for generator and a function to be called.",
)
@click.option(
    "--run",
    "-r",
    default=None,
    type=str,
    help="shell command to be run, example: `'echo {f}'`",
)
@click.option(
    "--nproc",
    "-n",
    type=int,
    default=mp.cpu_count(),
    help="number of processes for running command",
)
@click.option("--generator", "-g", default="-", help="")
@click.option(
    "-s", "--splitby", default=" ", type=str, help="character used for splitting input string"
)
@click.option(
    "--test",
    is_flag=True,
    help="Test mode, only run the first output from the generator",
)
@click.option("--subhelp", is_flag=True, help="get help doc from package")
@click.argument("params", nargs=-1, type=click.UNPROCESSED)
def main(params, pkg: Path, nproc: int, test: bool, generator, run, splitby, subhelp):
    if pkg is not None:
        pkg = load_from_file(pkg)

    if subhelp:
        doc = getattr(pkg, "__doc__", None)
        if doc:
            print("=== Script help === ")
            print(doc)
        if isinstance(getattr(pkg, "generator", None), click.Command):
            print("=== Generator help === ")
            pkg.generator(["--help"], standalone_mode=False)
        else:
            if generator:
                print("=== Generator help === ")
                print(generator)

        if run:
            doc = run
        elif hasattr(pkg, "run"):
            doc = getattr(pkg.run, "__doc__")
        if doc:
            print("=== Run help === ")
            print(doc)
        return

    if generator is not None:
        generator = get_default_generator(generator, splitby)
    elif pkg is not None and hasattr(pkg, "generator"):
        if isinstance(pkg.generator, click.Command):
            generator = pkg.generator(params, standalone_mode=False)
        else:
            generator = pkg.generator
    else:
        raise Exception("Can not identify generator")

    if run is not None:
        run = RunCmd(run)
    elif pkg is not None and hasattr(pkg, "run"):
        run = pkg.run
    else:
        raise Exception("Can not identify run")

    star = len(signature(run).parameters.keys()) > 1
    if test:
        generator = [(next(iter(generator)))]
    pool = mp.Pool(nproc)
    if star:
        result = pool.starmap(run, generator)
    else:
        result = pool.map(run, generator)


@cli.command()
@click.argument("index", type=int, default=-1)
def example(index):
    import pkgutil

    FOLDER = (
        Path(pkgutil.get_loader("pypara").get_filename()).absolute().parent / "examples"
    )
    if index == -1:
        for e in FOLDER.glob("example*"):
            print(e)
    else:
        with (FOLDER / f"example{index}.py").open() as fp:
            print(fp.read())


if __name__ == "__main__":
    cli()
