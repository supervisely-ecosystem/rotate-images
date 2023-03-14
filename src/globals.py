import os

import supervisely as sly

from dotenv import load_dotenv

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

TEAM_ID = sly.io.env.team_id()
WORKSPACE_ID = sly.io.env.workspace_id()
PROJECT_ID = sly.io.env.project_id()
PROJECT_INFO = api.project.get_info_by_id(id=PROJECT_ID)
DATASET_ID = sly.io.env.dataset_id()
DATASET_INFO = api.dataset.get_info_by_id(id=DATASET_ID)

SLY_APP_DATA_DIR = sly.app.get_data_dir()
STATIC_DIR = os.path.join(SLY_APP_DATA_DIR, "images")
os.makedirs(STATIC_DIR, exist_ok=True)
