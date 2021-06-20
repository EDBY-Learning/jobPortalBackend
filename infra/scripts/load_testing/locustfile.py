import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def hello_world(self):
        self.client.get("/teacher/public_profile/9/")
        self.client.get("/teacher/public_profile/10/")

    def on_start(self):
        pass 