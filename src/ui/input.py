import os

import supervisely as sly
from supervisely.app.widgets import (
    Card,
    SelectDataset,
    Button,
    Checkbox,
    Container,
    DatasetThumbnail,
)

import src.globals as g
import src.ui.rotator as rotator
import src.ui.output as output

dataset_thumbnail = DatasetThumbnail()
dataset_thumbnail.hide()

load_button = Button("Load data")

lock_checkbox = Checkbox("Lock dataset")
lock_checkbox.hide()

selected_project = None
selected_dataset = None

if g.DATASET_ID and g.PROJECT_ID:
    # If the app was loaded from a dataset.
    sly.logger.debug("App was loaded from a dataset.")

    # Stting values to the widgets from environment variables.
    select_dataset = SelectDataset(default_id=g.DATASET_ID, project_id=g.PROJECT_ID)

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

    selected_project = g.PROJECT_ID

    select_dataset = SelectDataset(
        project_id=g.PROJECT_ID, compact=True, show_label=False
    )
else:
    # If the app was loaded from ecosystem: showing the dataset selector in full mode.
    sly.logger.debug("App was loaded from ecosystem.")

    select_dataset = SelectDataset()


card = Card(
    "1️⃣ Input dataset",
    "Images from the selected dataset will be loaded.",
    content=Container(
        widgets=[lock_checkbox, select_dataset, load_button, dataset_thumbnail]
    ),
)


@load_button.click
def load_dataset():
    # Disabling the dataset selector and the load button.
    select_dataset.disable()
    load_button.disable()

    # Showing the lock checkbox for unlocking the dataset selector and button.
    lock_checkbox.check()
    lock_checkbox.show()

    # Putting the placeholder image to the image preview and locking rotator and output cards.
    rotator.image_preview.set(title="", image_url=os.path.join("static", g.PLACEHOLDER))
    rotator.preview_card.lock()
    output.card.lock()

    # Reading the dataset id from SelectDataset widget.
    dataset_id = select_dataset.get_selected_id()

    # Changing the values of the global variables to access them from other modules.
    global selected_dataset
    selected_dataset = dataset_id

    global selected_project
    selected_project = g.api.dataset.get_info_by_id(dataset_id).project_id

    sly.logger.debug(f"Dataset id loaded from the selector: {dataset_id}")

    # Building the table with images from the selected dataset.
    rotator.build_table(dataset_id)
    rotator.table_card.unlock()


@lock_checkbox.value_changed
def unlock_input(checked):
    if not checked:
        select_dataset.enable()
        load_button.enable()
    else:
        select_dataset.disable()
        load_button.disable()
