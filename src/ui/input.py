import os

import supervisely as sly
from supervisely.app.widgets import (
    Card,
    SelectDataset,
    Button,
    Container,
    DatasetThumbnail,
    Text,
)

import src.globals as g
import src.ui.rotator as rotator
import src.ui.output as output

dataset_thumbnail = DatasetThumbnail()
dataset_thumbnail.hide()

load_button = Button("Load data")
change_dataset_button = Button("Change dataset", icon="zmdi zmdi-lock-open")
change_dataset_button.hide()

no_dataset_message = Text(
    "Please, select a dataset before clicking the button.",
    status="warning",
)
no_dataset_message.hide()

# Global variables to access them from other modules.
selected_team = None
selected_workspace = None
selected_project = None
selected_dataset = None

if g.DATASET_ID and g.PROJECT_ID:
    # If the app was loaded from a dataset.
    sly.logger.debug("App was loaded from a dataset.")

    # Stting values to the widgets from environment variables.
    select_dataset = SelectDataset(default_id=g.DATASET_ID, project_id=g.PROJECT_ID, allowed_project_types=[sly.ProjectType.IMAGES])

    selected_team = g.TEAM_ID
    selected_workspace = g.WORKSPACE_ID
    selected_project = g.PROJECT_ID
    selected_dataset = g.DATASET_ID

    # Hiding unnecessary widgets.
    select_dataset.hide()
    load_button.hide()

    # Creating a dataset thumbnail to show.
    dataset_thumbnail.set(
        g.api.project.get_info_by_id(g.PROJECT_ID),
        g.api.dataset.get_info_by_id(g.DATASET_ID),
    )
    dataset_thumbnail.show()
    rotator.build_table(g.DATASET_ID)
    rotator.table_card.unlock()
elif g.PROJECT_ID:
    # If the app was loaded from a project: showing the dataset selector in compact mode.
    sly.logger.debug("App was loaded from a project.")

    selected_team = g.TEAM_ID
    selected_workspace = g.WORKSPACE_ID
    selected_project = g.PROJECT_ID

    select_dataset = SelectDataset(
        project_id=g.PROJECT_ID, compact=True, show_label=False, allowed_project_types=[sly.ProjectType.IMAGES]
    )
else:
    # If the app was loaded from ecosystem: showing the dataset selector in full mode.
    sly.logger.debug("App was loaded from ecosystem.")

    select_dataset = SelectDataset(allowed_project_types=[sly.ProjectType.IMAGES])

# Inout card with all widgets.
card = Card(
    "1️⃣ Input dataset",
    "Images from the selected dataset will be loaded.",
    content=Container(
        widgets=[
            dataset_thumbnail,
            select_dataset,
            load_button,
            change_dataset_button,
            no_dataset_message,
        ]
    ),
)


@load_button.click
def load_dataset():
    """Handles the load button click event. Reading values from the SelectDataset widget,
    calling the API to get project, workspace and team ids (if they're not set),
    building the table with images and unlocking the rotator and output cards.
    """
    # Reading the dataset id from SelectDataset widget.
    dataset_id = select_dataset.get_selected_id()

    if not dataset_id:
        # If the dataset id is empty, showing the warning message.
        no_dataset_message.show()
        return
    
    g.DATASET_CHANGING = True

    # Hide the warning message if dataset was selected.
    no_dataset_message.hide()

    # Hiding the result message after the new dataset is selected.
    output.result_message.hide()

    # Changing the values of the global variables to access them from other modules.
    global selected_dataset
    selected_dataset = dataset_id

    # Cleaning the static directory when the new dataset is selected.
    clean_static_dir()

    # Disabling the dataset selector and the load button.
    select_dataset.disable()
    load_button.hide()

    # Clearing the table if the new dataset was loaded.
    rotator.rows.clear()

    # Showing the lock checkbox for unlocking the dataset selector and button.
    change_dataset_button.show()

    # Putting the placeholder image to the image preview and locking rotator and output cards.
    rotator.image_preview.set(url=os.path.join("static", g.PLACEHOLDER))
    rotator.preview_card.lock()
    output.card.lock()

    global selected_team, selected_workspace, selected_project
    sly.logger.debug(
        f"Calling API with dataset ID {dataset_id} to get project, workspace and team IDs."
    )

    selected_project = g.api.dataset.get_info_by_id(dataset_id).project_id
    selected_workspace = g.api.project.get_info_by_id(selected_project).workspace_id
    selected_team = g.api.workspace.get_info_by_id(selected_workspace).team_id

    sly.logger.debug(
        f"Recived IDs from the API. Selected team: {selected_team}, "
        f"selected workspace: {selected_workspace}, selected project: {selected_project}"
    )

    dataset_thumbnail.set(
        g.api.project.get_info_by_id(selected_project),
        g.api.dataset.get_info_by_id(selected_dataset),
    )
    dataset_thumbnail.show()

    # Building the table with images from the selected dataset.
    rotator.build_table(dataset_id)
    rotator.table_card.unlock()

    g.DATASET_CHANGING = False


def clean_static_dir():
    """Deletes all files from the static directory except the placeholder image."""
    static_files = os.listdir(g.STATIC_DIR)

    sly.logger.debug(
        f"Cleaning static directory. Number of files to delete: {len(static_files) - 1}."
    )

    for static_file in static_files:
        if static_file != g.PLACEHOLDER:
            os.remove(os.path.join(g.STATIC_DIR, static_file))


@change_dataset_button.click
def unlock_input():
    """Handles the change dataset button click event. Enabling the dataset selector
    and the load button, hiding the change dataset button.
    """
    select_dataset.enable()
    load_button.show()
    change_dataset_button.hide()
