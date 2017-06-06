from PushBase import PushBase
from HydraConfig import HydraConfig
from json import dumps


class HydraPush(PushBase):
    def __init__(self):
        PushBase.__init__(self, HydraConfig())

    def run(self):
        try:
            # set status to REBUILD
            self.set_source_status('REBUILD')

            # crawl here...
            # for each document, create a document_id (uri), and a body, here is an example
            document_id = "MY DOCUMENT ID"
            body = dumps({
                "FileExtension": ".html",
                "CompressedBinaryData": self.compress_and_encode_data(self, "MY CONTENT HERE"),
                "connectortype": "CUSTOM MADE CONNECTOR (Or any other name)",
                "title": "MY TITLE HERE",
                "metadata1": "value1",
                "metadata2": "value2",
                "date": "DATE OF THE DOCUMENT",
                "Permissions": [{
                    "PermissionSets": [{
                        "AllowAnonymous": False,
                        "AllowedPermissions": [{
                            "IdentityType": "User",
                            "Identity": "jecloutier@athenahealth.com"
                        }],
                        "DeniedPermissions": []
                    }]
                }]
            })

            # Then, add the document
            self.add_document(self, document_id, body)

            # set status back to IDLE
            self.set_source_status('IDLE')
        except Exception as e:
            self.set_source_status('ERROR')

            raise e