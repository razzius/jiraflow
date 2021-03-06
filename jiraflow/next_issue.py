#!/usr/bin/env python3

"""\
Usage:

$ source ./read_jira_credentials
$ ./next_issue.py
"""

import os
import sys
from json.decoder import JSONDecodeError
from pprint import pprint

import requests

from jiraflow.lib import JIRA_SEARCH_URL, OPEN_ISSUES_JQL

process_name = sys.argv[0]


def error_out(response, message):
    print(f'{process_name}: {message}')
    print(f'Got response code {response.status_code}')
    exit(1)


def help_message(env):
    print('Missing ${env}'.format(env=env))
    error_out(__doc__)


def debug_response(response):
    pprint(response.json())


def main():
    authorization = os.environ.get('JIRA_AUTH')
    if authorization is None:
        help_message('JIRA_AUTH')

    response = requests.get(
        JIRA_SEARCH_URL,
        params={'jql': OPEN_ISSUES_JQL, 'maxResults': 1},
        headers={'Authorization': authorization},
    )

    if not response.ok:
        debug_response(response)

    if response.status_code == 400:
        error_out(response, 'inactive account or invalid query')

    if response.status_code == 401:
        error_out('bad password')

    try:
        print(response.json()['issues'][0]['key'].lower())
    except JSONDecodeError:
        print('{}: Bad auth'.format(process_name))
        exit(1)


if __name__ == '__main__':
    main()
