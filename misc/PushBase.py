import requests
import zlib
import base64
import shelve
from json import loads

class PushBase:
    def __init__(self, configuration):
        self.configuration = configuration

        # Create the urls and headers
        self.coveo_document_api_url = self.configuration.get_document_api_url()
        self.coveo_headers = self.configuration.get_headers_with_push_api_key()

    # Set the source status
    def set_source_status(self, status):
        # create statusType querystring parameter
        params = {
            'statusType': status
        }

        coveo_status_api_url = self.configuration.get_status_api_url()
        coveo_headers = self.configuration.get_headers_with_push_api_key()

        # print request
        print 'Calling: POST ' + coveo_status_api_url
        print 'statusType: ' + status

        # make POST request to change status
        r = requests.post(coveo_status_api_url, headers=self.coveo_headers, params=params)

        print r.status_code

    @staticmethod
    def compress_and_encode_data(self, data):
        return base64.b64encode(
            zlib.compress(
                data.encode('utf8'),
                zlib.Z_BEST_COMPRESSION
            )
        )

    def add_document(self, document_id, document_body):
        # create documentId querystring parameter
        params = {
            'documentId': document_id
        }

        #print request
        print '\nCall: PUT ' + self.coveo_document_api_url
        print 'Headers: ' + str(self.coveo_headers)
        print 'Params: ' + str(params)
        print 'Body: ' + document_body

        r = requests.put(
            self.coveo_document_api_url,
            headers=self.coveo_headers,
            params=params,
            data=document_body
        )

        if r.status_code == 202:
            print 'SUCCESS [%s]' % document_id
        else:
            print r.text

    # Set the source status
    def delete_older_than(self, epoch_time_in_milliseconds):
        coveo_delete_older_than_url = self.configuration.get_delete_older_thanurl(epoch_time_in_milliseconds)
        coveo_headers = self.configuration.get_headers_with_push_api_key()

        # print request
        print 'Calling: DELETE ' + coveo_delete_older_than_url

        r = requests.delete(coveo_delete_older_than_url, headers=self.coveo_headers)

        print r.status_code

    def push_batch(self, batch):
        coveo_get_batch_file_id_url = self.configuration.get_batch_file_id_url()

        # print request
        print 'Calling: POST ' + coveo_get_batch_file_id_url
        r = loads(
            requests.post(
                coveo_get_batch_file_id_url,
                headers=self.coveo_headers
            ).content
        )

        upload_uri = r["uploadUri"]
        file_id = r["file_id"]

        # Upload the batch
        specific_headers = self.coveo_headers
        specific_headers["Content Type"] = "application/octet-stream"
        specific_headers["x-amz-server-side-encryption"] = "AES256"

        print 'Calling: PUT ' + upload_uri
        r = requests.put(
            upload_uri,
            headers=specific_headers,
            data=batch
        )

        if r.status_code == 202:
            print 'SUCCESS [%s]' % file_id
        else:
            print r.text

        # Request the push api to process the batch
        coveo_batch_document_api_url = self.configuration.get_batch_document_api_url(file_id)
        print 'Calling: PUT ' + coveo_batch_document_api_url
        r = requests.put(
            coveo_get_batch_file_id_url,
            headers=self.configuration.get_headers_for_s3()
        )

        if r.status_code == 200:
            print 'SUCCESS [%s]' % file_id
        else:
            print r.text

    @staticmethod
    def print_rejects(reject_list):
        for reject in reject_list:
            print reject[0]
            print reject[1]

    @staticmethod
    def get_state_value(caller, key):
        shelf = shelve.open(str(caller.__class__.__name__) + ".shelf")
        value = shelf[key] if shelf.has_key(key) else None
        shelf.close()

        return value

    @staticmethod
    def set_state_value(caller, key, value):
        shelf = shelve.open(str(caller.__class__.__name__) + ".shelf")
        shelf[key] = value
        shelf.close()
