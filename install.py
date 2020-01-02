#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from itertools import zip_longest
from subprocess import check_output

base_path = os.path.dirname(os.path.realpath(__file__))


def num_common_parts(a, b):
    for i, (x, y) in enumerate(zip_longest(a.parts, b.parts)):
        if x != y:
            return i
    return len(a.parts)


def relative_to(a, b):
    num_common = num_common_parts(a, b)
    parts = [".."] * (len(b.parts) - num_common)
    parts.extend(a.parts[num_common:])
    return Path(*parts)


def confirm(prompt, *, default):
    while True:
        yn = input(prompt)
        if not yn:
            yn = "y" if default else "n"
        if yn.lower() in ("y", "n"):
            return yn.lower() == "y"


def install_pkg(pkg_name):
    pkg_path = Path(base_path, pkg_name)

    setup_path = Path(pkg_path, "setup")

    for root, _, files in os.walk(pkg_path):
        for file in files:
            path = Path(root, file)
            if path == setup_path:
                continue
            rel_path = path.relative_to(pkg_path)
            link_path = Path.home() / rel_path
            link_target = relative_to(path, link_path.parent)
            if link_path.is_symlink():
                link_path.unlink()
            if not link_path.parent.is_dir():
                link_path.parent.mkdir(parents=True, exist_ok=True)
            if link_path.exists():
                if not confirm(
                    f"File {link_path} alreday exists, delete it? [Y/n] ", default=True
                ):
                    continue
                link_path.unlink()
            link_path.symlink_to(link_target)
    if setup_path.exists():
        check_output([str(setup_path)])


pkg_names = sys.argv[1:]
if not pkg_names and confirm(
    "Do you want to install all packages? [Y/n] ", default=True
):
    pkg_names = set(os.listdir()) - {".git", "install.py"}


for pkg in pkg_names:
    print(f"Installing {pkg}")
    install_pkg(pkg)
