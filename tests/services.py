from datetime import datetime
from operator import itemgetter
from settings import JIRA_PROJECT_KEY, JIRA_USERNAME, JIRA_PASSWORD, JIRA_URL

import requests


def get_current_time():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


class TestServiceInterface():
    def get_issue_info(self):
        raise NotImplementedError()

    def get_tests_in_issue(self):
        raise NotImplementedError()

    def get_tests_in_folder(self):
        raise NotImplementedError()

    def create_test(self):
        raise NotImplementedError()

    def delete_test(self):
        raise NotImplementedError()

    def create_test_cycle(self):
        raise NotImplementedError()


class JiraTestService(TestServiceInterface):
    def __init__(self, jira_settings):
        self.project_key = jira_settings['project_key']
        self.auth_string = (jira_settings['user'], jira_settings['password'])
        self.url = jira_settings['url'] + '/rest/atm/1.0'
        self.issue_url = jira_settings['url'] + '/rest/api/latest/issue'
        self.folder = jira_settings['url'] + '/rest/atm/1.0/folder'

    def get_issue_info(self, issue_key):
        return requests.get(url=self.issue_url + '/' + issue_key,
                            auth=self.auth_string).json()

    def get_tests_in_issue(self, issue_key):
        params = {
            'query':
            'projectKey = "%s" AND issueKeys IN (%s)' %
            (self.project_key, issue_key)
        }
        response = requests.get(url=self.url + '/testcase/search',
                                params=params,
                                auth=self.auth_string).json()
        print(response)
        return list(map(itemgetter('name', 'key'), response))

    def get_tests_in_folder(self, folder_path):
        params = {
            'query': 'projectKey = "%s" AND folder = "%s"' % (self.project_key, folder_path)
        }
        response = requests.get(url=self.url+ '/testcase/search',
                                params=params,
                                auth=self.auth_string).json()
        print(response)
        return list(map(itemgetter('name', 'key'), response))

    def create_test(self, issue_key, test):
        json = {
            'name': test['name'],
            'projectKey': self.project_key,
            'issueLinks': [issue_key],
            'objective': test['objective'],
            'testScript': test['testScript'],
            'status': 'Approved',
            'folder': test['folder']
        }
        response = requests.post(url=self.url + '/testcase',
                                 json=json,
                                 auth=self.auth_string)
        test_key = response.json()['key']
        return test_key

    def delete_test(self, test_key):
        requests.delete(url=self.url + '/testcase/' + test_key,
                        auth=self.auth_string)

    def create_test_cycle(self, issue_key, name, items):
        json = {
            'name': name,
            'projectKey': self.project_key,
            'issueKey': issue_key,
            'plannedStartDate': get_current_time(),
            'plannedEndDate': get_current_time(),
            'items': items
        }
        requests.post(url=self.url + '/testrun',
                      json=json,
                      auth=self.auth_string)
    def transition_status_task(self, issue_key):
        json = {
            'transition': {
                'id': '701'
            }
        }
        requests.post(url=self.issue_url + '/' + issue_key + '/transitions?expand=transitions.fields',
                      json=json,
                      auth=self.auth_string)
    def create_test_folder(self, folder_name):
        json = {
            'projectKey': self.project_key,
            'name': folder_name,
            'type': 'TEST_CASE'
        }
        requests.post(url=self.folder,
                      json=json,
                      auth=self.auth_string)


def jira_test_service():
    return JiraTestService({
        'url': JIRA_URL,
        'user': JIRA_USERNAME,
        'password': JIRA_PASSWORD,
        'project_key': JIRA_PROJECT_KEY
    })
