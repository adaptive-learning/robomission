"""Configuration for a load testing using Locust.

To start load testing, run `make server` and `make test-load`.
"""
import random
from json.decoder import JSONDecodeError
from django.urls import reverse
from locust import HttpLocust, TaskSet, task


class SolvingTaskBehavior(TaskSet):
    """Describes interaction of a simulated user with a single task.

    The users requests a randomly choosen task,
    then she does random number of edits and unsuccessful executions,
    and finally she solves the task.
    """
    SOLVE_PROBABILITY = 0.3

    def on_start(self):
        selected_task = random.choice(self.parent.task_names)
        self.start_task(selected_task)

    def start_task(self, task_name):
        url = self.parent.action_urls['start_task']
        data = {'task':  task_name}
        response = self.parent.post_with_cookies(url, data)
        self.task_session_id = response.json()['task_session_id']
        self.edit_program()

    @task(1)
    def run_program(self):
        url = self.parent.action_urls['run_program']
        solved = random.random() < self.SOLVE_PROBABILITY
        data = {
            'task-session-id': self.task_session_id,
            'program': 'f',
            'correct': solved}
        self.parent.post_with_cookies(url, data)
        if solved:
            self.interrupt()

    @task(5)
    def edit_program(self):
        url = self.parent.action_urls['edit_program']
        data = {
            'task-session-id': self.task_session_id,
            'program': 'f'}
        self.parent.post_with_cookies(url, data)


class UserBehavior(TaskSet):
    """Describes interaction of a simulated user with the server.
    """
    tasks = [SolvingTaskBehavior]

    def __init__(self, parent):
        super().__init__(parent)
        self.cookies = {}
        self.action_urls = {}
        self.task_names = None

    def on_start(self):
        """Fill in cookies so that post request can be made later.
        """
        response = self.visit_homepage()
        self.save_cookies(response)
        self.save_tasks()
        self.save_action_urls()

    def visit_homepage(self):
        response = self.client.get('/')
        return response

    def save_tasks(self):
        response = self.client.get('/learn/api/tasks/')
        self.save_cookies(response)
        self.task_names = [task['name'] for task in response.json()]

    def save_action_urls(self):
        """The session and lazy user is created. Now tasks can be solved.
        """
        user_response = self.client.get('/learn/api/users/current')
        self.save_cookies(user_response)
        student_url = user_response.json()['student']
        student_response = self.client.get(student_url)
        self.save_cookies(student_response)
        self.action_urls['start_task'] = student_response.json()['start_task']
        self.action_urls['edit_program'] = student_response.json()['edit_program']
        self.action_urls['run_program'] = student_response.json()['run_program']

    def save_cookies(self, response):
        """Stores cookies for later usage.
        """
        self.cookies.update(response.cookies.get_dict())

    def post_with_cookies(self, url, data):
        """Post request with correctly set cookies and headers.
        """
        csrf_token = self.cookies['csrftoken']
        data['csrfmiddlewaretoken'] = csrf_token
        headers = {'X-CSRFToken': csrf_token, 'Referer': self.client.base_url}
        response = self.client.post(url, data, headers=headers, cookies=self.cookies)
        self.save_cookies(response)
        self.log_errors(response)
        return response

    @staticmethod
    def log_errors(response):
        if not response.ok:
            with open('request_errors.log', 'a') as f:
                f.writelines(response.text)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 5000
