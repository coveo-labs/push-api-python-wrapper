from PushConfiguration import PushConfiguration


class HydraConfig (PushConfiguration):
    crawling_user = "YOUR CRAWLING USER"
    list_url = "https://stageintranet-qad.company.com/hydra/api/1.0/lists?USER={crawling_user}"
    tasks_url = "https://stageintranet-qad.company.com/hydra/api/1.0/lists/{list_id}/tasks?USER={crawling_user}"
    task_display_url = "https://intranet.company.com/hydra/taskview.esp?ID={task_id}"

    def __init__(self):
        PushConfiguration.__init__(
            self,
            coveo_organization_id="YOUR ORG NAME",
            coveo_source_id="YOUR SOURCE ID",
            coveo_push_api_key="YOUR API KEY"
        )

    def get_list_url(self):
        return self.list_url.format(
            crawling_user=self.crawling_user
        )

    def get_tasks_url(self, list_id):
        return self.tasks_url.format(
            list_id=list_id,
            crawling_user=self.crawling_user
        )

    def get_task_display_url(self, task_id):
        return self.task_display_url.format(
            task_id=task_id
        )