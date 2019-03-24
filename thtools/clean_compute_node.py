#! /usr/bin/env python3

"""
Tools to cleanup scratch space on compute nodes

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

from collections import defaultdict
import getpass
import os
try:
    from pathlib import Path
    Path().expanduser()
except (ImportError, AttributeError):
    try:
        from pathlib2 import Path
    except ImportError:
        raise ImportError('Could not find the required pathlib/pathlib2\n'
                          'Try using Python >= 2.6')
try:
    from thtools import cd
except ImportError:
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


dict_node = {3: '/net/scc-{}',
             7: '/net/{}',
             12: '{}'}


def clean_node(node, print_list=True, rm='ask', subfolder=None):
    """
    Clean out scratch folder on a compute node.

    Note, this will not work with directories in the scratch folder. That
    will raise OSError.
    :param str node: Designation of the node on which to work.
        This accepts three different formats. For the node at
        '/net/scc-na1', any of the following will work: 'na1', 'scc-na1',
        or '/net/scc-na1'. It seems that capitalization may not matter,
        at least for the node name.
    :param bool print_list: Default: True. Print list of files.
        If True, the list of files (and directories) in the designated folder
        will be printed.
    :type rm: bool or str
    :param rm: Default: 'ask'. Delete the files.
        If True, the files will be deleted.
        If 'ask' (ignoring case), input from the user will be requested about
        whether to delete the files.
        If anything else, the files will not be deleted.
    :param str subfolder: Default: None. Subfolder of scratch directory in
        which to look.
        If subfolder is None, the user's username will be found with
        getpass.getuser() and that will be used as the subfolder.
    :return: None
    """
    try:
        _node = dict_node[len(node)].format(node)
    except KeyError:
        raise ValueError('Unable to parse node input "{}".\n Examples: "na1" |'
                         '"scc-na1" | "/net/scc-na1"')
    _subfolder = getpass.getuser() if subfolder is None else subfolder
    path = Path('{}/scratch/{}'.format(_node, _subfolder))
    if path.is_dir():
        paths = [path]
    else:
        p = path.parent
        paths = list(p.glob(_subfolder))
        if not paths:
            print('No folder: {}'.format(path))
            return None
    if isinstance(rm, bool):
        _rm = rm
    else:
        _rm = rm.lower()
    for path in paths:
        files = list(path.glob('*'))
        if len(files) == 0:
            print('No files in {}'.format(path))
            continue
        if print_list:
            print('The files in {} are:\n {}'.format(path, [f.name for f in
                                                            files]))
        response = False
        dict_response = defaultdict(lambda: False, y=True)
        if _rm is False:
            continue
        if _rm == 'ask':
            response = dict_response[input('Delete all files in '
                                           '{}? [yn]: '.format(path))]
        if response is True or _rm is True:
            for f in files:
                f.unlink()
        else:
            print('No files removed from "{}".'.format(path))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Clean out scratch folder on compute nodes')
    parser.add_argument('nodes', nargs='+', type=str,
                        help='Node or nodes on which to look for scratch files')
    p_group = parser.add_mutually_exclusive_group()
    p_group.add_argument('-p', '--print', action='store_true',
                         help='Default, print list of files')
    p_group.add_argument('-n', '--no_print', action='store_true',
                         help='Do not print the list of files')
    d_group = parser.add_mutually_exclusive_group()
    d_group.add_argument('-d', '--delete', action='store_true',
                         help='Delete the files without asking')
    d_group.add_argument('-a', '--ask', action='store_true',
                         help='Default, ask before deleting the files')
    parser.add_argument('-l', '--list_only', action='store_true',
                        help='Only list the files without deleting '
                             'anything. Note: this will override -d, but not '
                             '-a')
    parser.add_argument('-f', '--folder', type=str, default='',
                        help='Subfolder on node. Defaults to username')
    args = parser.parse_args()
    if args.ask or not (args.delete or args.ask or args.list_only):
        a_rm = 'ask'
    elif args.delete:
        a_rm = True
    else:
        a_rm = False
    _print = False if args.no_print else True
    a_subfolder = args.folder if args.folder else None
    for a_node in args.nodes:
        try:
            clean_node(a_node, print_list=_print, rm=a_rm,
                       subfolder=a_subfolder)
        except ValueError as e:
            print(e)
            print('continuing with rest...')
