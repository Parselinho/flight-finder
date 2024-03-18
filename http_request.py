import requests


class HttpRequester:
    def __init__(self, timeout=5):
        self.timeout = timeout

    def get(self, url, params=None, headers=None):
        return self._make_request("get", url, params=params, headers=headers)

    def post(self, url, json=None, headers=None):
        return self._make_request("post", url, json=json, headers=headers)

    def put(self, url, json=None, headers=None):
        return self._make_request("put", url, json=json, headers=headers)

    def _make_request(self, method, url, params=None, json=None, headers=None):
        try:
            response = requests.request(
                method,
                url,
                params=params,
                json=json,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("The request timed out.")
            return
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return
        except requests.exceptions.ConnectionError:
            print("Connection error occurred.")
            return
        except requests.exceptions.TooManyRedirects as err:
            print(f"Too many requests, try again later: {err}")
            return
        except requests.exceptions.RequestException as err:
            print(f"An unexpected error occurred: {err}")
            return
