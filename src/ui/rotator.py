import os
import secrets

from typing import List, Union, Tuple

import supervisely as sly

from supervisely.geometry.image_rotator import ImageRotator

from supervisely.app.widgets import (
    Card,
    Table,
    Container,
    Image,
    Slider,
    Field,
    Button,
    Flexbox,
    Checkbox,
)

import src.globals as g
import src.ui.input as input
import src.ui.output as output

# Global variable to store rotated angle value across the modules.
current_angle = 0

# Table columns names.
COL_ID = "IMAGE ID"
COL_IMAGE = "FILE NAME"
# COL_SIZE = "SIZE (BYTES)"
COL_WIDTH = "WIDTH (PIXELS)"
COL_HEIGHT = "HEIGHT (PIXELS)"
COL_LABELS = "LABELS (COUNT)"
COL_ROTATION = "ROTATION (DEGREES)"
SELECT_IMAGE = "SELECT"

columns = [
    COL_ID,
    COL_IMAGE,
    # COL_SIZE,
    COL_WIDTH,
    COL_HEIGHT,
    COL_LABELS,
    COL_ROTATION,
    SELECT_IMAGE,
]

# Global variable to store rows of the table.
rows = []

table = Table(fixed_cols=1, width="100%", per_page=15)
table.hide()

# Card with table widget (left side).
table_card = Card(
    "2️⃣ Select image",
    "Choose the image to rotate.",
    content=table,
    lock_message="Select a dataset on the step 1️⃣.",
)
table_card.lock()

image_preview = Image()
image_preview.set(url=os.path.join("static", g.PLACEHOLDER))

rotator = Slider(
    value=0,
    min=-180,
    max=180,
    step=1,
    show_input=True,
    show_input_controls=True,
)
rotator.set_value(current_angle)

rotate_left_button = Button("Rotate left", icon="zmdi zmdi-rotate-ccw")
rotate_right_button = Button("Rotate right", icon="zmdi zmdi-rotate-cw")

rotate_buttons = Flexbox(
    widgets=[rotate_left_button, rotate_right_button], center_content=True
)

precise_angle_checkbox = Checkbox(
    "Rotate the image with a precise angle", checked=False
)

apply_button = Button("Apply", icon="zmdi zmdi-check")
reset_button = Button("Reset", icon="zmdi zmdi-close", button_type="warning")
apply_flexbox = Flexbox(widgets=[apply_button, reset_button], center_content=True)


slider_field = Field(
    title="Rotate image with precise angle",
    description="Use the silder for rotating and then click the button to apply the angle.",
    content=Container(widgets=[rotator, apply_flexbox], direction="vertical"),
)
slider_field.hide()

# Card with all preview widgets (right side).
preview_card = Card(
    "3️⃣ Image preview",
    "The image will automatically update after changing the angle.",
    content=Container(
        [image_preview, rotate_buttons, precise_angle_checkbox, slider_field],
        direction="vertical",
    ),
    lock_message="Choose the image on the step 2️⃣.",
)
preview_card.lock()


@rotate_left_button.click
def rotate_left():
    """Rotates the image to the left by the angle specified in the global variable."""
    global current_angle
    rotate_angle = current_angle - g.ROTATE_ANGLE
    current_angle = rotate_angle
    rotate_preview(rotate_angle)


@rotate_right_button.click
def rotate_right():
    """Rotates the image to the right by the angle specified in the global variable."""
    global current_angle
    rotate_angle = current_angle + g.ROTATE_ANGLE
    current_angle = rotate_angle
    rotate_preview(rotate_angle)


@precise_angle_checkbox.value_changed
def precise_angle(checked: bool):
    """Shows the slider field when the checkbox is checked and hides it otherwise.

    Args:
        checked (_type_): current state of the checkbox.
    """
    if checked:
        slider_field.show()
        rotate_buttons.hide()
        rotator.set_value(current_angle)
    else:
        slider_field.hide()
        rotate_buttons.show()


@apply_button.click
def apply_angle():
    """Applies the angle specified in the slider to the image and rotates it."""
    rotator_angle = rotator.get_value()
    global current_angle
    current_angle = rotator_angle
    rotate_preview(rotator_angle)


@reset_button.click
def reset_angle():
    """Resets the angle to 0 and rotates the image to the original position."""
    rotator.set_value(0)
    global current_angle
    current_angle = 0
    rotate_preview(0)


def build_table(dataset_id: int):
    """Builds the table with images from the dataset.

    Args:
        dataset_id (int): the id of the dataset to build the table for.
    """
    global table, rows

    table.loading = True

    # Getting the list of images from the dataset.
    images = g.api.image.get_list(dataset_id)

    sly.logger.debug(
        f"Loaded {len(images)} images from the dataset with id {dataset_id}"
    )

    for image in images:
        rows.append(data_from_image(image))

    table_data = {"columns": columns, "data": rows}

    table.read_json(table_data)

    table.loading = False

    sly.logger.debug(f"Table with {len(images)} images was built successfully.")

    # Showing the table when the build is finished.
    table.show()


def data_from_image(image: sly.api.image_api.ImageInfo) -> List[Union[str, int]]:
    """Creates the row for the table from the ImageInfo object.

    Args:
        image (sly.api.image_api.ImageInfo): object containing the information about the image
        in Supervisely dataset.

    Returns:
        List[Union[str, int]]: image id, image name, image size, image width, image height,
        number of labels, button to select the image in the table
    """
    image_url = sly.imaging.image.get_labeling_tool_url(
        input.selected_team,
        input.selected_workspace,
        input.selected_project,
        input.selected_dataset,
        image.id,
    )

    return [
        image.id,
        f"<a href={image_url}>{image.name}</a>",
        # image.size,
        image.width,
        image.height,
        image.labels_count,
        image.meta.get("Rotated on angle", 0),
        sly.app.widgets.Table.create_button(SELECT_IMAGE),
    ]


# Global variables to access them in different functions.
# Image object loaded from the API.
current_image = None

# Name of file with random string to avoid caching.
random_image_name = None

# The path to the original image (which is not rotating until the Save button is clicked).
original_image_path = None

# Annotation object loaded from the API (which is also not rotating until the Save button is clicked).
original_annotation = None

# The path to the annotated image. Copies of this file will be created for each rotation.
annotated_image_path = None

# The path to the image which will be shown in the preview widget (it's the only one which actually rotating).
rotated_image_path = None


@table.click
def handle_table_button(datapoint: sly.app.widgets.Table.ClickedDataPoint):
    """Handles the click on the button in the table. Gets the image id from the
    table and calls the API to get the image info. Downloads the image to the static directory,
    reads the annotation info and shows the image in the preview widget.

    Args:
        datapoint (sly.app.widgets.Table.ClickedDataPoint): clicked datapoint in the table.
    """
    if g.SAVE_RUNNING is True:
        sly.logger.info(
            "The save process is in progress. Please wait until it's finished and you will be able to select another image."
        )
        return
    
    if g.DATASET_CHANGING is True:
        sly.logger.info("Dataset is changing. Please wait until it's finished and you will be able to select another image.")
        return

    if datapoint.button_name != SELECT_IMAGE:
        return

    # Resetting the global variables if the new image was selected.
    global current_image, original_image_path, original_annotation
    current_image = original_image_path = original_annotation = None
    global annotated_image_path, rotated_image_path, random_image_name
    annotated_image_path = rotated_image_path = random_image_name = None

    global current_angle
    current_angle = 0

    # Getting image id from the table after clicking the button.
    current_image_id = datapoint.row[COL_ID]
    # Getting image info from the dataset by image id.
    current_image = g.api.image.get_info_by_id(current_image_id)

    if not current_image:
        # If there was en error while getting the image info, deleting the row with the image id
        # and show the error message for the user.

        sly.logger.error(f"Can't find image with id {current_image_id} in the dataset.")
        sly.app.show_dialog(
            "Image not found",
            f"Can't find image with id {current_image_id} in the dataset.",
            status="error",
        )

        table.delete_row(COL_ID, current_image_id)

        sly.logger.debug(f"Deleted the row with id {current_image_id} from the table.")

        return

    sly.logger.debug(f"The image with id {current_image_id} was selected in the table.")

    # Creating a filename with random string to avoid caching.
    random_image_name = f"{secrets.token_hex(10)}_{current_image.name}"

    # Defining the path to the image in local static directory as global variable.
    original_image_path = os.path.join(g.STATIC_DIR, random_image_name)

    # Cleaning the static directory before downloading the image to avoid cached image in preview widget.
    input.clean_static_dir()

    # Downloading the image from the dataset to the local static directory.
    # It will be stored as original image without drawing the annotation on it.
    g.api.image.download(current_image_id, original_image_path)

    # Downloading the image as numpy array to add the annotation on it.
    image_np = g.api.image.download_np(current_image_id)

    sly.logger.debug(
        f"The image with id {current_image_id} was downloaded as numpy array."
    )

    # Getting project meta object from the dataset.
    meta_json = g.api.project.get_meta(input.selected_project)
    project_meta = sly.ProjectMeta.from_json(data=meta_json)

    # Getting annotation object from the dataset.
    ann_info = g.api.annotation.download(current_image_id)
    ann_json = ann_info.annotation

    # Defining the annotation object as global variable to save it after rotation.
    original_annotation = sly.Annotation.from_json(ann_json, project_meta)

    sly.logger.debug("Successfully read annotation for the image.")

    # Drawing the annotation on the image and saving it to the local static directory.
    preview_image_filename = f"annotated_{random_image_name}"
    annotated_image_path = os.path.join(g.STATIC_DIR, preview_image_filename)
    original_annotation.draw_pretty(image_np, output_path=annotated_image_path)

    sly.logger.debug(
        f"Drawn annotation on the image and saved it to {annotated_image_path}."
    )
    sly.logger.debug(f"The original image was saved to {original_image_path}.")

    # Updating the preview widget with rotated image.
    image_preview.set(
        url=os.path.join("static", preview_image_filename),
    )

    sly.logger.debug(
        f"Updated image preview with the image {preview_image_filename} from static directory."
    )

    rotator.set_value(0)
    preview_card.unlock()
    output.card.unlock()


def rotate_preview(angle: int):
    """Rotates the preview image by the given angle. Updates preview widget with the
    rotated image

    Args:
        angle (int): angle to rotate the preview image.
    """
    # Preparing widget for the new image.
    image_preview.clean_up()

    global current_angle

    if g.LEFT_LOCK_ANGLE <= current_angle <= g.RIGHT_LOCK_ANGLE:
        # Unlocking the buttons if the angle is in the allowed range.
        rotate_left_button.enable()
        rotate_right_button.enable()

        sly.logger.debug(f"Current angle is {current_angle}. Both buttons are enabled.")

    elif current_angle < g.LEFT_LOCK_ANGLE:
        # Locking the left button if the angle is less than the left lock angle.
        rotate_left_button.disable()

        sly.logger.debug(
            f"Current angle {current_angle} smaller than {g.LEFT_LOCK_ANGLE}. Left button is disabled."
        )

    elif current_angle > g.RIGHT_LOCK_ANGLE:
        # Locking the right button if the angle is more than the right lock angle.
        rotate_right_button.disable()

        sly.logger.debug(
            f"Current angle {current_angle} bigger than {g.RIGHT_LOCK_ANGLE}. Right button is disabled."
        )

    # Loading the image from the local static directory for rotation.
    global annotated_image_path
    img = sly.image.read(annotated_image_path)

    sly.logger.debug(
        f"Preview image was readed from path {annotated_image_path} in static directory."
    )

    # Rotating the image with inverted angle (just for convinient appearance in the GUI).
    # Using KEEP_BLACK mode to avoid data loss of the image.
    img = sly.image.rotate(img, -angle, mode=sly.image.RotateMode.KEEP_BLACK)

    sly.logger.debug(f"Image was rotated with angle {angle} degrees.")

    rotated_image_filename = f"rotated_{angle}_{random_image_name}"

    # Defining the path to the rotated image in local static directory as global variable.
    global rotated_image_path
    rotated_image_path = os.path.join(g.STATIC_DIR, rotated_image_filename)

    # Saving the rotated image to the local static directory.
    sly.image.write(rotated_image_path, img)

    sly.logger.debug(f"Rotated image was saved to {rotated_image_path}.")

    # Updating the image preview widget with new rotated image.
    image_preview.set(
        url=os.path.join("static", rotated_image_filename),
    )

    sly.logger.debug(
        f"Updated image preview with the rotated image {rotated_image_filename}."
    )


def rotate_image() -> Tuple[str, sly.Annotation]:
    """Reads global variables to load the original image and annotation, rotates them
    to a reversed angle and saves the result to the local static directory.

    Returns:
        Tuple[str, sly.Annotation]: local path to the rotated image and rotated annotation.
    """
    # Loading the original image from the local static directory.
    global current_angle, original_image_path, original_annotation
    original_image = sly.image.read(original_image_path)

    sly.logger.debug(
        f"Successfully read the original image from {original_image_path}."
    )

    # Rotating the image with inverted angle to correspond the angle in the preview widget.
    rotated_image = sly.image.rotate(
        original_image, -current_angle, mode=sly.image.RotateMode.KEEP_BLACK
    )

    sly.logger.debug(
        f"Successfully rotated the image with angle {-current_angle} degrees."
    )

    # Saving the rotated image to the local static directory.
    result_path = os.path.join(g.STATIC_DIR, f"result_{current_image.name}")
    sly.image.write(result_path, rotated_image)

    sly.logger.debug(f"Successfully saved the rotated image to {result_path}.")

    rotator = ImageRotator(original_annotation.img_size, -current_angle)
    result_annotation = original_annotation.rotate(rotator)

    sly.logger.debug(
        f"Successfully rotated the annotation with angle {-current_angle}."
    )

    return result_path, result_annotation
