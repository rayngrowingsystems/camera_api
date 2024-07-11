# Copyright 2024 RAYN Growing Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Example script - take a multispectral image and download the files and delete them from the camera
# NOTE: It is currently not possible to change the setting for the multispectral image
# the global setting of the camera are used

import api_v1

delete_images = True

if __name__ == "__main__":
    print("Taking multispectral image. This might take a while!")
    image_files = api_v1.take_ms_image()  # call function with default settings (see config.py)
    print("Done taking multispectral image")

    api_v1.download_files(file_list=image_files["files"], source=image_files["source"])

    if delete_images:
        print("Deleting downloaded files")
        for file in image_files["files"]:
            api_v1.delete_file(filename=file, source=image_files["source"])
