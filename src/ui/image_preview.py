import os

import supervisely as sly

from supervisely.app.widgets import Slider, Container, Field, Card, LabeledImage
from supervisely.geometry.image_rotator import ImageRotator

import src.ui.image_selector as image_selector
import src.globals as g

rotated_annotation = None
rotated_image_name = None
rotated_image_local_path = None

labeled_image = LabeledImage()

rotator = Slider(
    value=0,
    min=-180,
    max=180,
    step=1,
    show_input=True,
    show_input_controls=True,
)

controls_field = Field(
    title="Rotate image",
    description="Choose the angle for rotation.",
    content=rotator,
)

card = Card(
    "3️⃣ Image preview",
    "The image will automatically update after changing the angle.",
    content=Container(
        [labeled_image, controls_field],
        direction="vertical",
    ),
    lock_message="Choose the image on the step 2️⃣.",
)
card.lock()


@rotator.value_changed
def rotate_image(angle: int):
    labeled_image.clean_up()
    labeled_image.loading = True

    img = sly.image.read(image_selector.current_image_local_path)

    img = sly.image.rotate(img, angle, mode=sly.image.RotateMode.KEEP_BLACK)

    img_filename = os.path.basename(image_selector.current_image_local_path)

    rotated_image_filename = f"rotated_{angle}_{img_filename}"

    global rotated_image_name
    rotated_image_name = f"rotated_{angle}_{image_selector.current_image_name}"

    global rotated_image_local_path
    rotated_image_local_path = os.path.join(g.STATIC_DIR, rotated_image_filename)

    sly.image.write(rotated_image_local_path, img)
    rotator = ImageRotator(image_selector.current_image_annotation.img_size, angle)

    global rotated_annotation
    rotated_annotation = image_selector.current_image_annotation.rotate(rotator)

    labeled_image.set(
        title=image_selector.current_image.name,
        image_url=os.path.join("static", rotated_image_filename),
        ann=rotated_annotation,
    )
    labeled_image.loading = False
