from urllib3.util.retry import Retry

import requests
from requests.adapters import HTTPAdapter


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 5
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def get_adapter(config):
    session = requests.Session()
    assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
    session.hooks["response"] = [assert_status_hook]
    session.headers = config.PARAMS["headers"]
    retries = Retry(
        total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
    )
    session.mount(
        "http://",
        TimeoutHTTPAdapter(max_retries=retries, timeout=config.DEFAULT_TIMEOUT),
    )
    session.mount(
        "https://",
        TimeoutHTTPAdapter(max_retries=retries, timeout=config.DEFAULT_TIMEOUT),
    )
    return session
