#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

os.chdir(os.path.join(os.path.dirname(__file__), '..'));
sys.path.insert(0, os.getcwd());

from pathlib import Path;
import re;
import toml;
from typing import Any;
from typing import Optional;
from typing import Generator;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(path_toml: str, path_req: str):
    with open(path_toml, 'r') as fp:
        obj = toml.load(fp);
        project_name = get_package_name(obj);
        requirements = get_package_dependencies(obj);
    path = Path(path_req);
    # os.remove(path_req);
    path.touch();
    with open(path_req, 'w') as fp:
        for cond in filter_out_internal_references(requirements, name=project_name):
            fp.write(cond);
            fp.write('\n');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def filter_out_internal_references(
    req: list[str],
    name: Optional[str],
) -> Generator[str, None, None]:
    if name is None:
        yield from req;
    for cond in req:
        if re.match(pattern=f'^{name}(\\[(.*?)\\])?$', string=cond):
            continue;
        yield cond;
    return;

def get_package_name(obj: dict) -> Optional[str]:
    name = obj.get('project', {}).get('name', None);
    if not isinstance(name, str):
        return None;
    name = name.strip();
    if name == '':
        return None;
    return name;

def get_package_dependencies(obj: Any, force: bool = False) -> dict:
    req = [];
    if force and isinstance(obj, list):
        req += obj;
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if force or key == 'dependencies' or re.match(pattern=r'^.*[-\_]dependencies$', string=key, flags=re.IGNORECASE):
                req += get_package_dependencies(value, force=True);
            else:
                req += get_package_dependencies(value, force=force);
    return req;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    args = sys.argv[1:];
    path_toml = args[0] if len(args) >= 1 else 'pyproject.toml';
    path_req = args[1] if len(args) >= 2 else 'requirements.txt';
    main(path_toml=path_toml, path_req=path_req);
