class PushConfiguration:
    # Endpoints
    coveo_document_api_url = 'https://pushdev.cloud.coveo.com/v1/organizations/{organizationId}/sources/{sourceId}/documents'
    coveo_status_api_url = 'https://pushdev.cloud.coveo.com/v1/organizations/{organizationId}/sources/{sourceId}/status'

    def __init__(self, coveo_organization_id, coveo_source_id, coveo_push_api_key):
        # Coveo organization and source configuration
        self.coveo_organization_id = coveo_organization_id
        self.coveo_source_id = coveo_source_id
        self.coveo_push_api_key = coveo_push_api_key

    # construct Coveo API URLs
    def get_document_api_url(self):
        return self.coveo_document_api_url.format(
            organizationId = self.coveo_organization_id,
            sourceId = self.coveo_source_id
        )

    def get_status_api_url(self):
        return self.coveo_status_api_url.format(
            organizationId = self.coveo_organization_id,
            sourceId = self.coveo_source_id
        )

    # create Authorization (access_token) and content-type (json) headers
    def get_headers_with_push_api_key(self):
        return {
            'Authorization': 'Bearer ' + self.coveo_push_api_key,
            'content-type': 'application/json'
        }