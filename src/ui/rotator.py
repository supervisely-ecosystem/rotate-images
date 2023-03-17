import os

from typing import List, Union

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
COL_SIZE = "SIZE (BYTES)"
COL_WIDTH = "WIDTH (PIXELS)"
COL_HEIGHT = "HEIGHT (PIXELS)"
COL_LABELS = "LABELS (COUNT)"
SELECT_IMAGE = "SELECT"

columns = [
    COL_ID,
    COL_IMAGE,
    COL_SIZE,
    COL_WIDTH,
    COL_HEIGHT,
    COL_LABELS,
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
rotator.set_value(current_angle)

rotate_left_button = Button("Rotate left", icon="zmdi zmdi-undo")
rotate_right_button = Button("Rotate right", icon="zmdi zmdi-redo")

rotate_buttons = Flexbox(
    widgets=[rotate_left_button, rotate_right_button], center_content=True
)

precise_angle_checkbox = Checkbox("Rotate the image with precise angle", checked=False)

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
    rotate_image(rotate_angle)


@rotate_right_button.click
def rotate_right():
    """Rotates the image to the right by the angle specified in the global variable."""
    global current_angle
    rotate_angle = current_angle + g.ROTATE_ANGLE
    current_angle = rotate_angle
    rotate_image(rotate_angle)


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
    rotate_image(rotator_angle)


@reset_button.click
def reset_angle():
    """Resets the angle to 0 and rotates the image to the original position."""
    rotator.set_value(0)
    global current_angle
    current_angle = 0
    rotate_image(0)


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

    # df = pd.DataFrame(rows, columns=columns)
    # table.read_pandas(df)

    dict = {"columns": columns, "data": rows}

    table.read_json(dict)

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
        image.size,
        image.width,
        image.height,
        image.labels_count,
        sly.app.widgets.Table.create_button(SELECT_IMAGE),
    ]


# Global variables to access them in different functions.
current_image = None
current_image_local_path = None
rotated_image_local_path = None
current_image_annotation = None
rotated_annotation = None


@table.click
def handle_table_button(datapoint: sly.app.widgets.Table.ClickedDataPoint):
    """Handles the click on the button in the table. Gets the image id from the
    table and calls the API to get the image info. Downloads the image to the static directory,
    reads the annotation info and shows the image in the preview widget.

    Args:
        datapoint (sly.app.widgets.Table.ClickedDataPoint): clicked datapoint in the table.
    """
    if datapoint.button_name != SELECT_IMAGE:
        return

    # Resetting the global variables if the new image was selected.
    global current_image, current_image_local_path, current_image_annotation
    current_image = current_image_local_path = current_image_annotation = None
    global rotated_image_local_path, rotated_annotation
    rotated_image_local_path = rotated_annotation = None

    image_preview.loading = True

    # Getting image id from the table after clicking the button.
    current_image_id = datapoint.row[COL_ID]
    # Getting image info from the dataset by image id.
    current_image = g.api.image.get_info_by_id(current_image_id)

    sly.logger.debug(f"The image with id {current_image_id} was selected in the table.")

    # Defining the path to the image in local static directory as global variable.
    # global current_image_local_path
    current_image_local_path = os.path.join(g.STATIC_DIR, current_image.name)

    # Downloading the image from the dataset to the local static directory.
    g.api.image.download(current_image_id, current_image_local_path)

    sly.logger.debug(
        f"The image with id {current_image_id} was downloaded to {current_image_local_path}."
    )

    # Getting project meta object from the dataset.
    meta_json = g.api.project.get_meta(input.selected_project)
    project_meta = sly.ProjectMeta.from_json(data=meta_json)

    # Getting annotation object from the dataset.
    ann_info = g.api.annotation.download(current_image_id)
    ann_json = ann_info.annotation

    # Defining the annotation object as global variable to save it after rotation.
    # global current_image_annotation
    current_image_annotation = sly.Annotation.from_json(ann_json, project_meta)

    sly.logger.debug("Successfully read annotation for the image.")

    image_preview.set(
        title=current_image.name,
        image_url=os.path.join("static", current_image.name),
        ann=current_image_annotation,
    )

    sly.logger.debug(
        f"Updated image preview with the image {current_image.name} from static directory."
    )

    image_preview.loading = False

    rotator.set_value(0)
    preview_card.unlock()
    output.card.unlock()


def rotate_image(angle: int):
    """Rotates the image and annotation by the given angle. Updates preview widget with the
    rotated image and annotation.

    Args:
        angle (int): angle to rotate the image and annotation.
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
    img = sly.image.read(current_image_local_path)

    sly.logger.debug(
        f"Image was readed from path {current_image_local_path} in static directory."
    )

    # Rotating the image with inverted angle (just for convinient appearance in the GUI).
    # Using KEEP_BLACK mode to avoid data loss of the image.
    img = sly.image.rotate(img, -angle, mode=sly.image.RotateMode.KEEP_BLACK)

    sly.logger.debug(f"Image was rotated with angle {-angle} degrees.")

    rotated_image_filename = f"rotated_{-angle}_{current_image.name}"

    # Defining the path to the rotated image in local static directory as global variable.
    global rotated_image_local_path
    rotated_image_local_path = os.path.join(g.STATIC_DIR, rotated_image_filename)

    # Saving the rotated image to the local static directory.
    sly.image.write(rotated_image_local_path, img)

    sly.logger.debug(f"Rotated image was saved to {rotated_image_local_path}.")

    # Rotating the annotation with inverted angle (just for convinient appearance in the GUI).
    rotator = ImageRotator(current_image_annotation.img_size, -angle)

    # Defining the rotated annotation object as global variable to save it after rotation.
    global rotated_annotation
    rotated_annotation = current_image_annotation.rotate(rotator)

    sly.logger.debug("Annotation was successfully rotated.")

    # Updating the image preview widget with new rotated image and annotation.
    image_preview.set(
        title=current_image.name,
        image_url=os.path.join("static", rotated_image_filename),
        ann=rotated_annotation,
    )

    sly.logger.debug(
        f"Updated image preview with the rotated image {rotated_image_filename}."
    )
