from supervisely.app.widgets import Button, Card, Container, DestinationProject

import src.globals as g
import src.ui.image_preview as image_preview

destination = DestinationProject(workspace_id=g.WORKSPACE_ID, project_type="images")

save_button = Button("Save image")
card = Card(
    "4️⃣ Destination",
    "Select the output project and dataset.",
    collapsable=False,
    content=Container(widgets=[destination, save_button]),
    lock_message="Choose the image on the step 2️⃣.",
)
card.lock()


@save_button.click
def save_image():
    # project_id = destination.get_selected_project_id()
    dataset_id = destination.get_selected_dataset_id()

    if not image_preview.rotated_image_local_path:
        return
    rotated_image_id = g.api.image.upload_path(
        dataset_id,
        image_preview.rotated_image_name,
        image_preview.rotated_image_local_path,
    ).id
    print(rotated_image_id)
    if image_preview.rotated_annotation:
        g.api.annotation.upload_ann(rotated_image_id, image_preview.rotated_annotation)
