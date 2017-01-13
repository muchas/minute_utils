import json
from pytest import fixture


@fixture
def json_client(client):
    def method(name):
        def wrapper(self, url, data=None, **kwargs):
            if data:
                kwargs['data'] = json.dumps(data)
            if 'content_type' not in kwargs:
                kwargs['content_type'] = 'application/json'
            if 'auth_token' in kwargs:
                kwargs['HTTP_AUTHORIZATION'] = 'JWT {}'.format(kwargs['auth_token'])

            return getattr(client, name)(url, **kwargs)
        return wrapper

    class JsonClient(object):
        get = method('get')
        post = method('post')
        put = method('put')
        patch = method('patch')
        delete = method('delete')

    return JsonClient()
