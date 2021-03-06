"""
A context manager for changing directories

"""
########################################################################
#                                                                      #
# This script was written by Thomas Heavey in 2017.                    #
#        theavey@bu.edu     thomasjheavey@gmail.com                    #
#                                                                      #
# Copyright 2017 Thomas J. Heavey IV                                   #
#                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");      #
# you may not use this file except in compliance with the License.     #
# You may obtain a copy of the License at                              #
#                                                                      #
#    http://www.apache.org/licenses/LICENSE-2.0                        #
#                                                                      #
# Unless required by applicable law or agreed to in writing, software  #
# distributed under the License is distributed on an "AS IS" BASIS,    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or      #
# implied.                                                             #
# See the License for the specific language governing permissions and  #
# limitations under the License.                                       #
#                                                                      #
########################################################################

import os
from contextlib import contextmanager


@contextmanager
def cd(new_dir, ignore_blank=False):
    prev_dir = os.getcwd()
    if not ignore_blank or new_dir:
        os.chdir(os.path.expanduser(new_dir))
    try:
        yield
    finally:
        os.chdir(prev_dir)


def resolve_path(f, *dirs):
    """
    Try to find `f` here or in `dirs`; return absolute path to `f` if found

    If `f` is not found in `dirs`, it is return as-is.

    This also will search as if it's already an absolute path then in the
    current directory before looking in `dirs`.

    :param str f: The file to be searched for
    :param list(str) dirs: List of directories in which to search.
    :return: The absolute path to `f`.
    :rtype: str
    """
    _dirs = ['', './']
    _dirs += dirs
    for d in _dirs:
        path = os.path.join(d, f)
        if os.path.isfile(path):
            return os.path.abspath(path)
    return f
