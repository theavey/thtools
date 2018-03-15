"""
Functions for saving fairly arbitrary python objects

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
import pickle


def save_obj(obj, name):
    path = _make_path(name)
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    return path


def load_obj(name):
    if '.pkl' in name:
        path = name
    else:
        path = _make_path(name)
    with open(path, 'rb') as f:
        return pickle.load(f)


def make_obj_dir(directory='./'):
    try:
        os.makedirs(directory+'obj')
    except OSError as e:
        if e.errno == 17:
            pass  # catch and ignore FileExistsError (or the Py2 equivalent)
        else:
            raise

def _make_path(name):
    d, b = os.path.split(name)
    return os.path.join(d, 'obj/', b + '.pkl')

