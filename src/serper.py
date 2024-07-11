import json
from http import client as http_client

from config import config

# ------------------------------------------------ | find websites  | ------------------------------------------------


class SerperService:
    """Find sites that match your search"""

    serper_url: str = "google.serper.dev"

    def request_to_serper(self, query: str):
        connection = self._make_connection()
        payload = self._get_payload(query=query)
        response = self._get_response(connection=connection, payload=payload)
        data = self._parse_response(response)
        return data

    def _make_connection(self):
        return http_client.HTTPSConnection(host=self.serper_url)

    @staticmethod
    def _get_payload(query: str):
        return json.dumps({
            "q": query
        })

    def _get_response(self, connection, payload):
        connection.request("POST", "/search", payload, self._headers)
        response = connection.getresponse()
        return response

    @property
    def _headers(self):
        return {
            "X-API-KEY": config.SERPER_API_KEY,
            "Content-Type": "application/json"
        }

    @staticmethod
    def _parse_response(response):
        data = response.read()
        data = json.loads(data.decode("utf-8"))
        return data
