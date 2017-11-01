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
import os
import getpass
from . import cd


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
    if subfolder is None:
        _subfolder = getpass.getuser()
    else:
        _subfolder = subfolder
    path = '{}/{}'.format(_node, _subfolder)
    with cd(path):
        files = os.listdir('./')
        if print_list:
            print('The files in {} are:\n {}'.format(path, files))
        response = False
        dict_response = defaultdict(lambda : False, y=True)
        if rm.lower() == 'ask':
            response = dict_response[input('Delete all files in '
                                           '{}? [yn]: '.format(path))]
        if response is True or rm is True:
            for name in files:
                os.remove(name)
        else:
            print('None of the files removed from "{}".'.format(path))


# TODO add if __name__ == __main__ functionality
