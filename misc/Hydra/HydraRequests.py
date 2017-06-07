import requests
from HydraConfig import HydraConfig
from json import loads


class HydraRequests:
    def __init__(self):
        self.configuration = HydraConfig()

    def get_lists(self):
        return loads(
            requests.get(
            self.configuration.get_list_url(),
            verify=False
            )
            .content
        )["data"]

    def get_tasks(self, list_id):
        return loads(
            requests.get(
            self.configuration.get_tasks_url(list_id),
            verify=False
            )
            .content
        )["data"]
    
