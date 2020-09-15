import requests
import os

from .nanodegree import Nanodegree
from .course import Course


class Session:
    def __init__(self, token):
        self._sess = requests.Session()
        self.update_token(token)

    def update_token(self, token):
        self._token = token
        self._sess.headers['Authorization'] = f"Bearer {token}"

    @classmethod
    def login(cls, email, password):
        resp = requests.post('https://user-api.udacity.com/signin', json={
            "email": email,
            "password": password,
            "otp": "",
            "next": "https://classroom.udacity.com/authenticated"
        })

        token = resp.cookies['_jwt']
        return cls(token)

    @property
    def token(self):
        return self._token

    def request(self, *args, **kwargs):
        return self._sess.request(*args, **kwargs)


class GraphQLRequest:
    def __init__(self, sess):
        self._sess = sess

    def request_(self, filename, *args):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, filename)) as f:
            query = f.read() % args
        url = 'https://classroom-content.udacity.com/api/v1/graphql'
        resp = self._sess.request(method='POST', url=url, json={
            "query": query,
            "variables": None,
            "locale": "en-us"
        })

        return resp.json()

    def send_request(self, kind, id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, f'udacity-{kind}.graphql')) as f:
            query = f.read() % id
        url = 'https://classroom-content.udacity.com/api/v1/graphql'
        resp = self._sess.request(method='POST', url=url, json={
            "query": query,
            "variables": None,
            "locale": "en-us"
        })
        if resp.status_code // 100 != 2:
            raise Exception(resp)
        obj = resp.json()
        data = obj['data'][kind]
        return data

    def get_course(self, id) -> Course:
        data = self.send_request('course', id)
        return Course(data)

    def get_nanodegree(self, id):
        data =  self.send_request('nanodegree', id)
        return Nanodegree(data)
