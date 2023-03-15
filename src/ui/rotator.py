import os

import pandas as pd
import supervisely as sly

from supervisely.geometry.image_rotator import ImageRotator

from supervisely.app.widgets import (
    Card,
    Table,
    Container,
    LabeledImage,
    Slider,
    Field,
    Button,
    Flexbox,
)

import src.globals as g
import src.ui.input as input
import src.ui.output as output

COL_ID = "image id".upper()
COL_IMAGE = "image".upper()
COL_SIZE = "size (bytes)".upper()
COL_WIDTH = "width (pixels)".upper()
COL_HEIGHT = "height (pixels)".upper()
COL_LABELS = "labels (count)".upper()
SELECT_IMAGE = "select".upper()

columns = [COL_ID, COL_IMAGE, COL_SIZE, COL_WIDTH, COL_HEIGHT, COL_LABELS, SELECT_IMAGE]

table = Table(fixed_cols=1, width="100%", per_page=15)
table.hide()

table_card = Card(
    "2️⃣ Select image",
    "Choose the image to rotate.",
    content=table,
    lock_message="Select a dataset on the step 1️⃣.",
)
table_card.lock()

image_preview = LabeledImage()
image_preview.set(title="", image_url=os.path.join("static", g.PLACEHOLDER))

rotator = Slider(
    value=0,
    min=-180,
    max=180,
    step=1,
    show_input=True,
    show_input_controls=True,
)

rotate_left_button = Button("Rotate left", icon="fa:undo")
rotate_right_button = Button("Rotate right", icon="fa:repeat")

rotate_buttons = Flexbox(
    widgets=[rotate_left_button, rotate_right_button], center_content=True
)

controls_field = Field(
    title="Rotate image",
    description="Choose the angle for rotation.",
    content=Container(widgets=[rotator, rotate_buttons], direction="vertical"),
)

preview_card = Card(
    "3️⃣ Image preview",
    "The image will automatically update after changing the angle.",
    content=Container(
        [image_preview, controls_field],
        direction="vertical",
    ),
    lock_message="Choose the image on the step 2️⃣.",
)
preview_card.lock()


@rotate_left_button.click
def rotate_left():
    current_angle = rotator.get_value()
    new_angle = current_angle - 90
    rotator.set_value(new_angle)


@rotate_right_button.click
def rotate_right():
    current_angle = rotator.get_value()
    new_angle = current_angle + 90
    rotator.set_value(new_angle)


def build_table(dataset_id: int):
    """Builds the table with images from the dataset.

    Args:
        dataset_id (int): the id of the dataset to build the table for.
    """
    global table

    # Clearing the table.
    rows = []

    table.loading = True

    # Getting the list of images from the dataset.
    images = g.api.image.get_list(dataset_id)

    sly.logger.debug(
        f"Loaded {len(images)} images from the dataset with id {dataset_id}"
    )

    for image in images:
        rows.append(
            [
                image.id,
                image.name,
                image.size,
                image.width,
                image.height,
                image.labels_count,
                sly.app.widgets.Table.create_button(SELECT_IMAGE),
            ]
        )

    df = pd.DataFrame(rows, columns=columns)
    table.read_pandas(df)
    table.loading = False

    sly.logger.debug("Table with images was built successfully.")

    # Showing the table when the build is finished.
    table.show()


# Global variables to access them in different functions.
current_image = None
current_image_local_path = None
rotated_image_local_path = None
current_image_annotation = None
rotated_annotation = None


@table.click
def handle_table_button(datapoint: sly.app.widgets.Table.ClickedDataPoint):
    global current_image
    if datapoint.button_name is None:
        return

    # Getting image id from the table after clicking the button.
    current_image_id = datapoint.row[COL_ID]
    # Getting image info from the dataset by image id.
    current_image = g.api.image.get_info_by_id(current_image_id)

    print(current_image_id)

    if datapoint.button_name == SELECT_IMAGE:
        # Defining the path to the image in local static directory as global variable.
        global current_image_local_path
        current_image_local_path = os.path.join(g.STATIC_DIR, current_image.name)

        # Downloading the image from the dataset to the local static directory.
        g.api.image.download(current_image_id, current_image_local_path)

        # Getting project meta object from the dataset.
        meta_json = g.api.project.get_meta(input.selected_project)
        project_meta = sly.ProjectMeta.from_json(data=meta_json)

        # Getting annotation object from the dataset.
        ann_info = g.api.annotation.download(current_image_id)
        ann_json = ann_info.annotation

        # Defining the annotation object as global variable to save it after rotation.
        global current_image_annotation
        current_image_annotation = sly.Annotation.from_json(ann_json, project_meta)

        image_preview.set(
            title=current_image.name,
            image_url=os.path.join("static", current_image.name),
            ann=current_image_annotation,
        )
        rotator.set_value(0)

        preview_card.unlock()
        output.card.unlock()
        image_preview.show()


@rotator.value_changed
def rotate_image(angle: int):
    # Preparing widget for the new image.
    image_preview.clean_up()

    if g.LEFT_LOCK_ANGLE <= angle <= g.RIGHT_LOCK_ANGLE:
        rotate_left_button.enable()
        rotate_right_button.enable()
    elif angle < g.LEFT_LOCK_ANGLE:
        rotate_left_button.disable()
    elif angle > g.RIGHT_LOCK_ANGLE:
        rotate_right_button.disable()

    # Loading the image from the local static directory for rotation.
    img = sly.image.read(current_image_local_path)

    # Rotating the image with inverted angle (just for convinient appearance in the GUI).
    # Using KEEP_BLACK mode to avoid data loss of the image.
    img = sly.image.rotate(img, -angle, mode=sly.image.RotateMode.KEEP_BLACK)

    rotated_image_filename = f"rotated_{angle}_{current_image.name}"

    # Defining the path to the rotated image in local static directory as global variable.
    global rotated_image_local_path
    rotated_image_local_path = os.path.join(g.STATIC_DIR, rotated_image_filename)

    # Saving the rotated image to the local static directory.
    sly.image.write(rotated_image_local_path, img)

    # Rotating the annotation with inverted angle (just for convinient appearance in the GUI).
    rotator = ImageRotator(current_image_annotation.img_size, -angle)

    # Defining the rotated annotation object as global variable to save it after rotation.
    global rotated_annotation
    rotated_annotation = current_image_annotation.rotate(rotator)

    # Updating the image preview widget with new rotated image and annotation.
    image_preview.set(
        title=current_image.name,
        image_url=os.path.join("static", rotated_image_filename),
        ann=rotated_annotation,
    )
