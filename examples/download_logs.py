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

# Example script - download the logs and delete them from the camera

import api_v1

delete_logs = True
source = "service"

if __name__ == "__main__":
    log_files = api_v1.get_file_list(source=source)  # call function with default settings (see config.py)
    num_log_files = log_files["total"]

    print(f"Found {num_log_files} log files. Downloading them to folder {source}")

    api_v1.download_files(file_list=log_files["files"], source=log_files["source"])

    if delete_logs:
        print("Deleting downloaded logs")
        for file in log_files["files"]:
            api_v1.delete_file(filename=file, source=log_files["source"])

