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
    """"""  # TODO add docstring
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
