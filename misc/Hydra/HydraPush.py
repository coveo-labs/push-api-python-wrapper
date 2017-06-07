from PushBase import PushBase
from HydraConfig import HydraConfig
from HydraRequests import HydraRequests
from json import dumps
from time import time, sleep
from sys import argv


class HydraPush(PushBase):
    def __init__(self):
        PushBase.__init__(self, HydraConfig())
        self.configuration = HydraConfig()

    @staticmethod
    def build_task_body(self, task):
        # Build the metadata
        task["documentId"] = task["uri"]
        task["FileExtension"] = ".html"
        # We do not have any binary data for this source. But if we would have had, here's.
        # ... how I would have done it
        # task["CompressedBinaryData"] = self.compress_and_encode_data(self, "MY CONTENT")
        task["connectortype"] = "CUSTOM MADE HYDRA CONNECTOR"
        task["title"] = ""
        task["Permissions"] = [{
            "PermissionSets": [{
                "AllowAnonymous": True,
                "AllowedPermissions": [],
                "DeniedPermissions": []
            }]
        }]

        return dumps(task)

    def run(self):
        try:
            # Get the time so we can call the delete older than later
            epoch_time_in_milliseconds = int(round(time() * 1000))

            # set status to REBUILD
            self.set_source_status('REBUILD')

            requester = HydraRequests()

            reject_list = []

            for task_group_list in requester.get_lists():
                try:
                    if task_group_list["VIEWABLEBY"] != '*':
                        # we should do something with that information, like securing the documents...
                        print list["VIEWABLEBY"]
                    else:
                        pass

                    for task_group in requester.get_tasks(task_group_list["ID"]):
                        try:
                            batch = []

                            for task in task_group:
                                try:
                                    # Assign the uri
                                    task["uri"] = self.configuration.get_task_display_url(task["ID"])

                                    # Then, add the document

                                    batch.append(self.build_task_body(task))
                                except Exception as e:
                                    reject_list.append("TASK", e)

                            self.push_batch(
                                batch={
                                    "AddOrUpdate": batch,
                                    "Delete": []
                                }
                            )
                        except Exception as e:
                            reject_list.append(["TASK GROUP", e])
                except Exception as e:
                    reject_list.append(["LIST", e])

            # Delete old documents
            self.delete_older_than(epoch_time_in_milliseconds)

            # Save the state
            self.set_state_value(self, "lastupdatedatetime", epoch_time_in_milliseconds)

            # set status back to IDLE
            self.set_source_status('IDLE')

            # Display rejects
            for reject in reject_list:
                print reject[0]
                print reject[1]
        except Exception as e:
            self.set_source_status('ERROR')

            raise e

    def run_incremental(self):
        # Get the state
        last_update_epoch_time_in_milliseconds = self.get_state_value(self, "lastupdatedatetime")

        if last_update_epoch_time_in_milliseconds is None:
            # No last update found, warn that we will start an initial build...
            print "WARNING: NO LAST UPDATE DATETIME FOUND."
            for x in range(10):
                print "Will start an initial build in {seconds} seconds".format(seconds=str(10-x))
                sleep(1)

            # Run the initial build
            self.run()
        else:
            try:
                # Get the time so we can call the delete older than later
                epoch_time_in_milliseconds = int(round(time() * 1000))

                # set status to REBUILD
                self.set_source_status('REFRESH')

                requester = HydraRequests()

                reject_list = []

                for task_group_list in requester.get_lists():
                    try:
                        if task_group_list["VIEWABLEBY"] != '*':
                            # we should do something with that information, like securing the documents...
                            print list["VIEWABLEBY"]
                        else:
                            pass

                        for task_group in requester.get_tasks(task_group_list["ID"]):
                            try:
                                for task in task_group:
                                    try:
                                        # Assign the uri
                                        task["uri"] = self.configuration.get_task_display_url(task["ID"])

                                        # Then, add the document
                                        self.add_document(
                                            task["uri"],
                                            self.build_task_body(task)
                                        )
                                    except Exception as e:
                                        reject_list.append("TASK", e)
                            except Exception as e:
                                reject_list.append(["TASK GROUP", e])
                    except Exception as e:
                        reject_list.append(["LIST", e])

                # Delete old documents
                self.delete_older_than(epoch_time_in_milliseconds)

                # Save the state
                self.set_state_value(self, "lastupdatedatetime", epoch_time_in_milliseconds)

                # set status back to IDLE
                self.set_source_status('IDLE')

                # Display rejects
                for reject in reject_list:
                    print reject[0]
                    print reject[1]
            except Exception as e:
                self.set_source_status('ERROR')

                raise e

if __name__ == "__main__":
    pusher = HydraPush()

    if len(argv) > 1:
        if str(argv[1]).lower() == "incremental":
            pusher.run_incremental()
    else:
        pusher.run()
