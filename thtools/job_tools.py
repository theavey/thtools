"""
Functions helpful for some job management and such

"""
########################################################################
#                                                                      #
# This script was written by Thomas Heavey in 2018.                    #
#        theavey@bu.edu     thomasjheavey@gmail.com                    #
#                                                                      #
# Copyright 2018 Thomas J. Heavey IV                                   #
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
import re
import shlex
import subprocess


def get_node_mem(node=None):
    """
    Get an approximate max memory for current node in GB

    This also will scale by the number of processors assigned divided by the
    total number of processors for the given host node.
    For example, if the submitted job is only using 8 of a total of 16 cores
    on the node, this will return 90% of half of the node's total memory.

    :param str node: name of the node, such as 'scc-na1.scc.bu.edu'. If this
        is not given or set to None, it will be taken from the environment
        variable HOSTNAME.
    :return: 90% of the memory available, likely in GB
    :rtype: int
    """
    n_slots = float(os.environ['NSLOTS'])
    if node is None:
        node = os.environ['HOSTNAME']
    cl = shlex.split('qconf -se {}'.format(node))
    proc = run(cl)
    m_proc = re.search(r'num_proc=(\d+)', proc.stdout)
    if m_proc is None:
        raise ValueError('Could not find n_proc for {}'.format(node))
    p_of_c = n_slots / float(m_proc.group(1))
    m = re.search(r'mem_total=(\d+\.\d+)M', proc.stdout)
    return int(float(m.group(1)) * 0.90 * p_of_c / 1000.)


def running_jobs_names(user=None):
    """
    Return the list of job names for a certain user

    :param str user: The user to list the jobs for. If user is None,
        the current user will be taken from the environment variable USER.
    :return: A list of the names of the currently running jobs
    :rtype: list
    """
    if user is None:
        user = os.environ['USER']
    j_ns = []
    proc = run(['qstat', '-r', '-u', user])
    for line in proc.stdout.splitlines():
        if 'Full jobname' in line:
            m = re.search(r'Full jobname:\s+(\S+)', line)
            j_ns.append(m.group(1))
    return j_ns


def run(cl):
    """
    Use subprocess.run with the given command line and (my) standard options

    Note, unfortunately, subprocess.run was only available starting in py3.5,
    and I don't particularly feel like re-writing it right now. Maybe there's
    some easy way to fix this that I'm not thinking of right now (import from
    future? literally copy and paste its definition?)

    :param list cl: Command line argument as a list of strings (e.g.,
    as returned by shlex.split).
    :return: The CompletedProcess instance
    :rtype: subprocess.CompletedProcess
    """
    return subprocess.run(cl,
                          universal_newlines=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
