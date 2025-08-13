import os

from datetime import datetime

import supervisely as sly

from supervisely.app.widgets import Button, Card, Container, Select, Text

import src.ui.input as input
import src.globals as g
import src.ui.rotator as rotator

result_message = Text()
result_message.hide()

# Generating the list of items for the save method widget fom the dictionary.
save_method = Select(
    items=[Select.Item(value=key, label=value) for key, value in g.SAVE_METHODS.items()]
)

save_button = Button("Save image")

# Card with all output widgets.
card = Card(
    "4️⃣ Save method",
    "Choose how to save the image and press the button.",
    collapsable=False,
    content=Container(widgets=[save_method, save_button, result_message]),
    lock_message="Choose the image on the step 2️⃣.",
)
card.lock()


def disable_controls():
    input.load_button.disable()
    input.change_dataset_button.disable()
    rotator.table.disable()
    rotator.rotate_left_button.disable()
    rotator.rotate_right_button.disable()
    rotator.precise_angle_checkbox.disable()
    rotator.apply_button.disable()
    rotator.reset_button.disable()
    rotator.rotator.disable()


def enable_controls():
    input.load_button.enable()
    input.change_dataset_button.enable()
    rotator.table.enable()
    rotator.rotate_left_button.enable()
    rotator.rotate_right_button.enable()
    rotator.precise_angle_checkbox.enable()
    rotator.apply_button.enable()
    rotator.reset_button.enable()
    rotator.rotator.enable()


@save_button.click
def save_image():
    """Saves the rotated image to the dataset if it was rotated. If the image was not rotated, shows the error message.
    Reading the dataset id from the input widget. If the save method is to create a new image, generates a new name for
    the image to avoid non unique exception. If the save method is to replace the current image,
    removes the current image from the dataset and deletes the row with the current image from the table.
    After that, saves the rotated image to the dataset and adds the row with the new image to the table.
    Generates a message with the result of the rotation and a link to the image in the labeling tool.
    """
    g.SAVE_RUNNING = True
    result_message.hide()
    disable_controls()

    # Getting the id of the dataset from the inout widget.
    dataset_id = input.selected_dataset

    sly.logger.debug(f"Readed dataset id from the widget: {dataset_id}")

    # Checking if the image was rotated.
    if rotator.current_angle == 0:
        result_message.text = "The image was not rotated."
        result_message.status = "error"

        result_message.show()

        sly.logger.info("The save button was pressed, but the image was not rotated.")
        enable_controls()
        return

    # Getting the save method from the save method widget.
    create_new_image = save_method.get_value()
    sly.logger.debug(
        f"The save method is to create a new image: {create_new_image is True}."
    )

    # Reading the original file and the annotation and rotating them to the current angle.
    result_path, result_annotation = rotator.rotate_image()

    if create_new_image:
        # Changing the name of the image to avoid non unique exception.
        image_postfix = 1
        image_name = rotator.current_image.name

        # Splitting the image name to the base name and the extension to paste the postfix.
        image_filename, image_extension = os.path.splitext(image_name)

        sly.logger.debug(
            f"Splitted image name. Base name: {image_filename}; Extension: {image_extension}."
        )

        while g.api.image.exists(dataset_id, image_name):
            # Generating a new name for the image if it already exists in the dataset.
            sly.logger.debug(
                f"Image with name {image_name} already exists in the dataset with id {dataset_id}."
            )

            image_name = (
                f"{image_filename}_{str(image_postfix).zfill(3)}{image_extension}"
            )
            image_postfix += 1

            sly.logger.debug(f"Generated new image name: {image_name}.")

        result_message.text = "Successfully created a new image with name: {image_url}."

    else:
        # Getting the id of the current image and removing it from the dataset.
        image_id = rotator.current_image.id
        g.api.image.remove(image_id)

        sly.logger.info(
            f"Removed the image with id {image_id} from the dataset with id {dataset_id}"
        )

        # Deleting the row with the current image from the table.

        try:
            rotator.table.delete_row(rotator.COL_ID, image_id)
            sly.logger.debug(
                f"Deleted the row with image id {image_id} from the column {rotator.COL_ID}"
            )
        except Exception as e:
            sly.logger.warning(f"Can not delete row for column ID: {rotator.COL_ID}")

        # Using the same name for the image since it was removed from the dataset.
        image_name = rotator.current_image.name

        result_message.text = "Successfully replaced the image with name: {image_url}."

    # Adding iformation about the rotation to the image metadata.
    meta = rotator.current_image.meta
    rotate_meta = {
        "Rotated on time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Rotated on angle": rotator.current_angle,
    }
    meta.update(rotate_meta)

    sly.logger.debug(f"Image metadata was updated with rotation data: {rotate_meta}.")

    # Uploading the rotated image to the dataset.
    rotated_image_id = g.api.image.upload_path(
        dataset_id,
        image_name,
        result_path,
        meta,
    ).id

    sly.logger.info(
        f"Uploaded the rotated image with id {rotated_image_id} to the dataset with id {dataset_id}."
    )

    # Uploading annotation for the rotated image.
    g.api.annotation.upload_ann(rotated_image_id, result_annotation)

    sly.logger.info(
        f"Uploaded the annotation for the image with id {rotated_image_id}."
    )
    # Getting ImageInfo after the image was uploaded and annotation was added.
    rotated_image = g.api.image.get_info_by_id(rotated_image_id)

    # Getting the link to the labeling tool for the rotated image to show it in the result message.
    image_url = sly.imaging.image.get_labeling_tool_url(
        input.selected_team,
        input.selected_workspace,
        input.selected_project,
        input.selected_dataset,
        rotated_image.id,
    )

    sly.logger.debug(
        f"Generated the link to the labeling tool for the rotated image: {image_url}."
    )

    # Formatting the result message with the link to the rotated image in the labeling tool.
    result_message.text = result_message.text.format(
        image_url=f'<a href="{image_url}">{rotated_image.name}</a>'
    )

    result_message.status = "success"
    result_message.show()

    # Adding the row with the rotated image to the table and updating it.
    rotator.table.loading = True

    rotator.table.insert_row(rotator.data_from_image(rotated_image))

    sly.logger.debug(f"Added the row with image id {rotated_image.id} to the table.")

    rotator.table.loading = False
    enable_controls()
    g.SAVE_RUNNING = False
