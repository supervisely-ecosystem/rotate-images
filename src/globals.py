import os
import shutil

import supervisely as sly

from dotenv import load_dotenv

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()

TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()

PROJECT_ID = sly.env.project_id(raise_not_found=False)
DATASET_ID = sly.env.dataset_id(raise_not_found=False)

SLY_APP_DATA_DIR = sly.app.get_data_dir()
ABSOLUTE_PATH = os.path.dirname(__file__)

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
