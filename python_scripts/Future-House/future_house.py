from futurehouse_client import FutureHouseClient, JobNames
from pathlib import Path
from aviary.core import DummyEnv
import ldp

api_key_file = Path("api_key.txt")

with api_key_file.open("r", encoding="utf-8") as file:
    api_key = file.read().strip()

client = FutureHouseClient(
    api_key=api_key,
)

task_data = {
    "name": JobNames.CROW,
    "query": "Which neglected diseases had a treatment developed by artificial intelligence?",
}

task_response = client.run_tasks_until_done(task_data)
