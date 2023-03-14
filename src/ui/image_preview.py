import os

from PIL import Image as PILImage
from supervisely.app.widgets import Image, Slider, Container, Field, Card, LabeledImage

import src.ui.image_selector as image_selector
import src.globals as g

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
    title="Controls",
    description="Placeholder for descrp",
    content=rotator,
)

card = Card(
    "3️⃣ Image preview",
    "Placeholder for descrp",
    content=Container(
        [labeled_image, controls_field],
        direction="vertical",
    ),
    lock_message="placeholder 2️⃣",
)
card.lock()


@rotator.value_changed
def rotate_image(angle: int):
    labeled_image.clean_up()
    labeled_image.loading = True
    img = PILImage.open(image_selector.current_image_local_path)
    img = img.rotate(angle, expand=True)

    img_filename = os.path.basename(image_selector.current_image_local_path)
    rotated_img_filename = f"rotated_{angle}_{img_filename}"

    img.save(os.path.join(g.STATIC_DIR, rotated_img_filename))
    labeled_image.set(
        title=image_selector.current_image.name,
        image_url=os.path.join("static", rotated_img_filename),
    )
    labeled_image.loading = False
