#!/usr/bin/env python3

"""
This script copies all subfolders into the user space

This is only required on the Dartmouth JupyterHub, where the repo is
mounted as read-only.
"""

import argparse
from pathlib import Path
import shutil
from typing import List


def script_location() -> Path:
    """Returns the location of this script (i.e. the repo root)"""
    return Path(__file__).parent.resolve()


def subfolders(source: Path) -> List[Path]:
    """
    Returns a list of the subfolders below source

    Excludes hidden folders (e.g. '.git').
    """
    return [x for x in source.iterdir() if x.is_dir() and not x.name.startswith(".")]


def copy(
    source: Path, destination: Path, verbose: bool = False, preserve: bool = False
):
    """
    Copies a directory tree to a new root
    """
    for file in source.rglob("*.*"):
        if file.parent == source:
            if verbose:
                print(f"Only subfolders of {source} are copied! Skipping file {file}.")
            continue
        if file.name.startswith("."):
            if verbose:
                print(f"Skipping hidden file {file}.")
            continue
        new_path = set_new_root(file, source, destination)
        if preserve and new_path.exists():
            if verbose:
                print(f"Preserving existing file {new_path}. Skipping.")
            continue
        new_path.parents[0].mkdir(parents=True, exist_ok=True)
        shutil.copy(file, new_path)


def set_new_root(path: Path, old_root: Path, new_root: Path) -> Path:
    """
    Sets a path to a new root

    Example:

    path = "~/some/old_root/path/to/folder/"
    new_root = "~/new_root"

    returns "~/new_root/path/to/folder/"
    """
    return new_root / path.relative_to(old_root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="Increase output verbosity", action="store_false"
    )
    parser.add_argument(
        "-p",
        "--preserve",
        help="Preserve existing files in user space",
        action="store_true",
    )
    args = parser.parse_args()

    print("Setting up user home folder...")
    cwd = script_location()
    copy(
        cwd, Path.home() / "RR-workshops", verbose=args.verbose, preserve=args.preserve
    )
    print("...done.")
