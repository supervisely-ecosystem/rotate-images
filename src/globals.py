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

# Defining the path to the directory where the images will be saved and creating it if it doesn't exist.
STATIC_DIR = os.path.join(SLY_APP_DATA_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Copying the placeholder image to the static directory.
PLACEHOLDER = "placeholder.png"
dst_file = os.path.join(STATIC_DIR, PLACEHOLDER)
shutil.copy(PLACEHOLDER, dst_file)

# Rotation constants. Locks are used to disable the rotation buttons when the image is rotated to the maximum angle.
ROTATE_ANGLE = 90
LEFT_LOCK_ANGLE = -90
RIGHT_LOCK_ANGLE = 90

# Constants for the image saving methods.
# Replace will delete the original image and upload the rotated one with the same name.
# Create will upload the rotated image using the number in postfix to the original image name.
SAVE_METHODS = {0: "Replace the image", 1: "Create a new image"}
