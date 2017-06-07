class PushConfiguration:
    # Endpoints
    base_url = "https://push.cloud.coveo.com/v1/organizations/{organization_id}/"
    coveo_document_api_url = base_url + "sources/{source_id}/documents"
    coveo_status_api_url = base_url + "sources/{source_id}/status"
    coveo_delete_older_than_url = base_url + "sources/{source_id}/documents/olderthan?orderingId={ordering_id}"
    coveo_get_batch_file_id_url = base_url + "files"
    coveo_batch_document_api_url = base_url + "sources/{source_id}/documents/batch?fileId={file_id}"

    def __init__(self, coveo_organization_id, coveo_source_id, coveo_push_api_key):
        # Coveo organization and source configuration
        self.coveo_organization_id = coveo_organization_id
        self.coveo_source_id = coveo_source_id
        self.coveo_push_api_key = coveo_push_api_key

    # construct Coveo API URLs
    def get_document_api_url(self):
        return self.coveo_document_api_url.format(
            organization_id=self.coveo_organization_id,
            source_id=self.coveo_source_id
        )

    def get_status_api_url(self):
        return self.coveo_status_api_url.format(
            organization_id=self.coveo_organization_id,
            source_id=self.coveo_source_id
        )

    def get_batch_file_id_url(self):
        return self.coveo_get_batch_file_id_url.format(
            organization_id=self.coveo_organization_id
        )

    def get_batch_document_api_url(self, file_id):
        return self.coveo_batch_document_api_url.format(
            organization_id=self.coveo_organization_id,
            source_id=self.coveo_source_id,
            file_id=file_id
        )

    def get_delete_older_than_url(self, epoch_time_in_milliseconds):
        return self.coveo_delete_older_than_url.format(
            organization_id=self.coveo_organization_id,
            source_id=self.coveo_source_id,
            ordering_id=epoch_time_in_milliseconds
        )

    # create Authorization (access_token) and content-type (json) headers
    def get_headers_with_push_api_key(self):
        return {
            'Authorization': 'Bearer ' + self.coveo_push_api_key,
            'content-type': 'application/json'
        }
