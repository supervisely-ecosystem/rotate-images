import supervisely as sly

from supervisely.app.widgets import Button, Card, Container, Select, Text

import src.ui.input as input
import src.globals as g
import src.ui.rotator as rotator

result_message = Text()
result_message.hide()

save_method = Select(
    items=[Select.Item(value=key, label=value) for key, value in g.SAVE_METHODS.items()]
)

save_button = Button("Save image")
card = Card(
    "4️⃣ Save method",
    "Choose how to save the image and press the button.",
    collapsable=False,
    content=Container(widgets=[save_method, save_button, result_message]),
    lock_message="Choose the image on the step 2️⃣.",
)
card.lock()


@save_button.click
def save_image():
    result_message.hide()

    dataset_id = input.selected_dataset

    print(dataset_id)

    sly.logger.debug(f"Readed dataset id from the widget: {dataset_id}")

    if not rotator.rotated_image_local_path:
        result_message.text = "The image was not rotated."
        result_message.status = "error"

        sly.logger.info("The save button was pressed, but the image was not rotated.")

        return

    create_new_image = save_method.get_value()
    sly.logger.debug(
        f"The save method is to create a new image: {create_new_image is True}."
    )

    if create_new_image:
        # Changing the name of the image to avoid non unique exception.
        image_name = f"rotated_{rotator.current_image.name}"

        result_message.text = "Successfully created a new image."

    else:
        # Getting the id of the current image and removing it from the dataset.
        image_id = g.api.image.get_info_by_name(
            dataset_id, rotator.current_image.name
        ).id
        g.api.image.remove(image_id)

        sly.logger.info(
            f"Removed the image with id {image_id} from the dataset with id {dataset_id}"
        )

        image_name = rotator.current_image.name

        result_message.text = "Successfully updated the image."

    # Uploading the rotated image to the dataset.
    rotated_image_id = g.api.image.upload_path(
        dataset_id,
        image_name,
        rotator.rotated_image_local_path,
        rotator.current_image.meta,
    ).id

    sly.logger.info(
        f"Uploaded the rotated image with id {rotated_image_id} to the dataset with id {dataset_id}."
    )

    if rotator.rotated_annotation:
        # Uploading the annotation for the rotated image if it exists.
        g.api.annotation.upload_ann(rotated_image_id, rotator.rotated_annotation)

        sly.logger.info(
            f"Uploaded the annotation for the image with id {rotated_image_id}."
        )

    result_message.status = "success"
    result_message.show()

    rotator.build_table(dataset_id)
