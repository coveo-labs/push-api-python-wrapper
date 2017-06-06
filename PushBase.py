import json
import re
import requests
import sys
import zlib
import base64


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
        r = requests.post(coveo_status_api_url, headers=coveo_headers, params=params)

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


