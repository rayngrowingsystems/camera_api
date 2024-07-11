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

# Example script - downloads all image files taken in the last two days

import api_v1
import datetime

delete_images = True
set_source = "scheduler"

if __name__ == "__main__":

    end = datetime.datetime.now()  # get data/time end
    start = end - datetime.timedelta(days=2)

    end_iso = end.isoformat()
    start_iso = start.isoformat()

    file_list = api_v1.get_files_in_range(start_datetime=start_iso, end_datetime=end_iso, source=set_source)
    print("Found files: " + ", ".join(file_list["files"]))

    api_v1.download_files(file_list=file_list["files"], source=set_source)

    if delete_images:
        print("Deleting downloaded files")
        for file in file_list["files"]:
            api_v1.delete_file(filename=file, source=set_source)
