import supervisely as sly
from supervisely.app.widgets import Button, Card, Container, DestinationProject

import src.globals as g

destination = DestinationProject(workspace_id=g.WORKSPACE_ID, project_type="images")

save_button = Button("Save")
card = Card(
    "4️⃣ Output project",
    "Select output destination",
    collapsable=False,
    content=Container(widgets=[destination, save_button]),
    lock_message="placeholder 3️⃣",
)
