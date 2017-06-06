from json import dumps

from HydraConfig import HydraConfig
from HydraRequests import HydraRequests

from misc.PushBase import PushBase


class HydraPush(PushBase):
    def __init__(self):
        PushBase.__init__(self, HydraConfig())
        self.configuration = HydraConfig()

    def run(self):
        try:
            # set status to REBUILD
            self.set_source_status('REBUILD')

            requester = HydraRequests()

            for list in requester.get_lists():
                if list["VIEWABLEBY"] != '*':
                    print list["VIEWABLEBY"] # we should do something with that information, like securing the documents...
                else:
                    pass

                for task_group in requester.get_tasks(list["ID"]):
                    for task in task_group:
                        task["uri"] = self.configuration.get_task_display_url(task["ID"])
                        # Build the metadata
                        task["FileExtension"] = ".html"
                        # We do not have any binary data for this source. But if we would have had, here's...
                        # ... how I would have done it
                        # task["CompressedBinaryData"] = self.compress_and_encode_data(self, "MY CONTENT HERE")
                        task["connectortype"] = "CUSTOM MADE HYDRA CONNECTOR"
                        task["title"] = ""
                        task["Permissions"] = [{
                                "PermissionSets": [{
                                    "AllowAnonymous": True,
                                    "AllowedPermissions": [],
                                    "DeniedPermissions": []
                                }]
                            }]
                        body = dumps(task)

                        # Then, add the document
                        self.add_document(task["uri"], body)

            # Delete old documents
            self.delete_older_than_now()

            # set status back to IDLE
            self.set_source_status('IDLE')
        except Exception as e:
            self.set_source_status('ERROR')

            raise e

if __name__ == "__main__":
    pusher = HydraPush()
    pusher.run()
    
