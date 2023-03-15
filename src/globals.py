import os
import shutil

import supervisely as sly

from dotenv import load_dotenv

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

TEAM_ID = sly.io.env.team_id()
WORKSPACE_ID = sly.io.env.workspace_id()

PROJECT_ID = None
DATASET_ID = None

try:
    PROJECT_ID = sly.io.env.project_id()
except Exception:
    sly.logger.debug("Project id not found in env variables.")

try:
    DATASET_ID = sly.io.env.dataset_id()
except Exception:
    sly.logger.debug("Dataset id not found in env variables.")

SLY_APP_DATA_DIR = sly.app.get_data_dir()
STATIC_DIR = os.path.join(SLY_APP_DATA_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)
PLACEHOLDER = "placeholder.png"
dst_file = os.path.join(STATIC_DIR, PLACEHOLDER)
shutil.copy(PLACEHOLDER, dst_file)

LEFT_LOCK_ANGLE = -90
RIGHT_LOCK_ANGLE = 90

SAVE_METHODS = {0: "Update the image", 1: "Create a new image"}
