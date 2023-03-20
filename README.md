<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/115161827/225969759-5699c73c-fbac-4eb3-aa10-c66f9e375ca5.jpg"/>

# Rotate images with annotations

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Run">How To Use</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/rotate-images)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/rotate-images)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/rotate-images)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/rotate-images)](https://supervise.ly)

</div>

## Overview
This app allows you to rotate images along with annotations. After selecting a dataset to work with, the app will generate a table with all images in the dataset. You can open an image in the preview window and rotate it left or right and even on a custom angle with the slider. After rotating the image, you can save replace the original image with the rotated one or save it as a new image. The app will also rotate all annotations on the image.

**Warning! This app does not support working with Cuboids!**

## How To Run
The app can be launched from the context menu of a dataset or a project along with the option to be launched from Supervisely EcoSystem. If the app is launched from EcoSystem, you need to select a project and a dataset with images to work with.<br>
## How To Use

If you don't run the app from the context menu of a dataset, first of all you need to specify the dataset to work with. You need to select a dataset in the `Input dataset` section. After selecting the dataset, click the button `Load data` under the dataset selector. The app will load the dataset and generate a table with all images in the dataset.<br>
Note: when the data from the dataset will be loaded, the dataset selector will be locked until you click the `Change dataset` button.<br>
Now you can follow these steps to rotate images:<br>
<br>
**Step 1:** Сlick on the `SELECT` button in the rightmost column. The image will be opened in the preview window.<br>
_Hint: the image names in the table are clickable, which may help you to find the image you need to work with._<br><br>
**Step 2:** Now you can click rotate the selected image with buttons `Rotate left` and `Rotate right` or with the slider.<br>
_Hint: If you need to rotate the image on a custom angle, you can use the slider, which is hidden by default. To show the slider, check the `Rotate the image with a precise angle` checkbox. The rotate buttons will be hidden and the slider will be shown instead. You can reset the current image rotation by clicking the `Reset` button under the slider. The image will be rotated back to the original state._ <br><br>
**Step 3:** When you finish rotating the image, you can save the result. Follow the `Save method` section and choose one of two options: replace the original image with the rotated one or save the rotated image as a new file. After selecting the save method, click the `Save image` button.<br><br>

<img src="https://camo.githubusercontent.com/03071e926ee06fea57df612cdf42367ce8c50f2547d970a9ebcdf4204e231a71/68747470733a2f2f746f7572696e67637265772e636f6d2f696d675f73686172652f726f746174655f696d616765732e706e67"/> <br><br>

**Step 4:** The app will save the image to the _same dataset_ and will show the success message, which also contains the link to the image in the dataset. Note: if you didn't make any changes to the image, the app will show the error message and won't save the image.<br><br>

**Step 5:** After finishing using the app, don't forget to stop the app session manually in the Workspace tasks. The app will write information about the rotation angle, date and time of applying the rotation to the image metadata. You can find this information in the `Image properties - Info` section of the image in the labeling tool.<br>
