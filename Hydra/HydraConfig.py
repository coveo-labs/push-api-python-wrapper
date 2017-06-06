from PushConfiguration import PushConfiguration


class HydraConfig (PushConfiguration):
    def __init__(self):
        PushConfiguration.__init__(
            coveo_organization_id="",
            coveo_source_id="",
            coveo_push_api_key=""
        )