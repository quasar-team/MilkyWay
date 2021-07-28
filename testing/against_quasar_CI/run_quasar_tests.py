#!/usr/bin/env python3
'''
run_quasar_tests.py

@author:     Piotr Nikiel <piotr@nikiel.info>

@copyright:  2021 CERN

@license:
Copyright (c) 2021, CERN.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
   and the following disclaimer in the documentation and/or other materials provided with the
   distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT  HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS  OR
IMPLIED  WARRANTIES, INCLUDING, BUT NOT  LIMITED TO, THE IMPLIED WARRANTIES  OF  MERCHANTABILITY
AND  FITNESS  FOR  A  PARTICULAR  PURPOSE  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,  SPECIAL, EXEMPLARY, OR  CONSEQUENTIAL
DAMAGES (INCLUDING, BUT  NOT LIMITED TO,  PROCUREMENT OF  SUBSTITUTE GOODS OR  SERVICES; LOSS OF
USE, DATA, OR PROFITS; OR BUSINESS  INTERRUPTION) HOWEVER CAUSED AND ON ANY  THEORY  OF  LIABILITY,
WHETHER IN  CONTRACT, STRICT  LIABILITY,  OR  TORT (INCLUDING  NEGLIGENCE OR OTHERWISE)  ARISING IN
ANY WAY OUT OF  THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

@contact:    quasar-developers@cern.ch
'''

import argparse
import yaml
import os
import datetime
import math
import pygit2
import sys
from colorama import Fore, Style
import threading
import pdb
import re
from milkyway import Server
import time

def run_test(design, config=None, compare_with_nodeset=None):
    server = Server(os.path.join('quasar', design))
    if config:
        server.instantiate_from_config(config)
    server.start()
    time.sleep(3)
    os.system('uasak_dump --endpoint_url opc.tcp://127.0.0.1:4841')
    if compare_with_nodeset:
        ref_ns2_path = os.path.join('quasar', compare_with_nodeset)
        rv = os.system(f'~/gitProjects/NodeSetTools/nodeset_compare.py {ref_ns2_path} dump.xml --ignore_nodeids StandardMetaData')
        print(f'RV was: {rv}')
    server.stop()

def fetch_option(cmd, option):
    option_re = re.compile(r"--"+option+" ([^ ]*)")
    matches = option_re.search(cmd)
    if matches:
        return matches.groups(0)[0]
    else:
        return None

def parse_command(cmd):
    print(f'{Fore.YELLOW}parse_command{Style.RESET_ALL} {cmd}')
    cmd_re = re.compile(r"run_test_case\.py ([^;]*);")
    matches = cmd_re.search(cmd)
    if not matches:
        return
    test_cmd_line = matches.groups(0)[0]
    print(f'{Fore.BLUE}found cmd line{Style.RESET_ALL}: {test_cmd_line}')

    args_names = ['design', 'config', 'compare_with_nodeset']
    args = {name: fetch_option(test_cmd_line, name) for name in args_names}

    if args['design'] is None:
        print('Assuming default design because --design was not given')
        args['design'] = 'Design/Design.xml'

    for arg_name in args:
        print(f'{Fore.GREEN}{arg_name}{Style.RESET_ALL}: {args[arg_name]}')

    run_test(**args)


def main():
    if not os.path.isdir('quasar'):
        raise Exception('quasar directory not found. clone quasar')

    yaml_file = open('quasar/.travis.yml')
    yaml_repr = yaml.load(yaml_file)

    non_public_yaml_file = open('quasar/.CI/travis/non_public_tests.yml', 'r')
    non_public_yaml_repr = yaml.load(non_public_yaml_file)

    print(f"Note: loading {len(yaml_repr['jobs']['include'])} jobs from main travis file and "
        f"{len(non_public_yaml_repr['jobs']['include'])} jobs from non_public_tests")

    yaml_repr['jobs']['include'].extend(non_public_yaml_repr['jobs']['include'])

    job_names_in_yaml = [job['name'] for job in yaml_repr['jobs']['include']]
    print('note: jobs declared in the yaml are:', job_names_in_yaml)

    parser = argparse.ArgumentParser()
    parser.add_argument("--select-jobs", help="A comma-separated list of jobs to execute instead of all jobs", default = ','.join(job_names_in_yaml))
    # parser.add_argument("--no-term-reset", help="Dont reset the terminal", action='store_true')
    # parser.add_argument("--num-workers", default=3, type=int, help="Number of jobs to run concurrently.")
    args = parser.parse_args()

    job_names_selected = args.select_jobs.split(',')
    jobs_to_do = [job for job in yaml_repr['jobs']['include'] if job['name'] in job_names_selected]
    print('The following jobs were selected to be executed:', '\n'.join([job['name'] for job in jobs_to_do]))

    job_results = {}

    for job in jobs_to_do:
        print(f'At job {job["name"]}')
        cmd_list = job['script']
        for cmd in cmd_list:

            print('Lets execute: ' + cmd)
            parse_command(cmd)


if __name__ == "__main__":
    main()
