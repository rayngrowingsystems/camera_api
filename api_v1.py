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

import requests
import os
import config


def api_call(url, settings=None, data=None, timeout=config.API_V1_TIMEOUT):
    """
    Helper function to make API calls
    :param url: API URL
    :param settings: python dict with parameters
    :param data: only necessary to post/upload data
    :param timeout: sets the timeout in seconds
    :return: API response
    """
    response = None

    try:
        if data:
            response = requests.post(url,
                                     data=data,
                                     timeout=timeout,
                                     headers={"Content-Type": "application/octet-stream"})
            # header is octet-stream because we don't know what type it is
        else:
            response = requests.get(url, json=settings, timeout=timeout)

        response.raise_for_status()

    # error handling
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

    return response


def get_status(ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Get camera status (name, firmware version and timestamp)
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    :return: camera info (python dict)
    """
    status = None

    api_url = f"http://{ip_address}/api/v1/status?key={key}"

    response = api_call(api_url, timeout=timeout)  # Query system status

    if response and response.status_code == 200:
        # command successful
        status = response.json()
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")

    return status


def get_info(ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Get camera info (SD-card and health infos)
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    :return: camera info (python dict)
    """

    info = None

    api_url = f"http://{ip_address}/api/v1/info?key={key}"

    response = api_call(api_url, timeout=timeout)  # Query system information

    if response and response.status_code == 200:
        # command successful
        info = response.json()
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")

    return info


def trigger_camera_restart(ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Restarts camera
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    """
    # Restart module

    api_url = f"http://{ip_address}/api/v1/reset?key={key}"

    response = api_call(api_url, timeout=timeout)

    if response and response.status_code == 200:
        print("Reset in progress...")
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")


def flash_light(spectrum=1, brightness=200, time=1000,
                ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Flash LED light of a single specturm
    :param spectrum: 0-10, see README
    :param brightness: 0-1000
    :param time: duration of flash in ms
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    :return: all settings (python dict)
    """

    settings = {
        "spectrum": int(spectrum),
        "brightness": int(brightness),
        "time": int(time)
    }

    api_url = f"http://{ip_address}/api/v1/flashlight?key={key}"

    response = api_call(api_url, settings=settings, timeout=timeout)

    if response and response.status_code == 200:
        # command successful
        response = response.json()
        print(response)
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")

    return response


def get_file(filename, source, ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Get single file (helper function for download_files())
    :param filename: Name of the file that should be retrieved
    :param source: respective source folder (see README)
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    :return: file
    """

    settings = {
        "filename": filename,
        "source": source
    }

    file = None

    api_url = f"http://{ip_address}/api/v1/files/get?key={key}"

    response = api_call(api_url, settings=settings, timeout=timeout)

    if response and response.status_code == 200:
        # command successful
        file = response.content  # get the file
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")

    return file


def delete_file(filename, source, ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Deletes file from the camera
    :param filename: name of the file to be deleted
    :param source: respective file source folder (see README)
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    """

    settings = {
        "filename": filename,
        "source": source
    }

    api_url = f"http://{ip_address}/api/v1/files/delete?key={key}"

    response = api_call(api_url, settings=settings, timeout=timeout)  # delete file

    if response and response.status_code == 200:
        # command successful
        print(f"Deleted {filename}")
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")


def get_file_list(source, ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY,
                  timeout=config.API_V1_TIMEOUT, index=0, limit=500):
    """
    Receive a full file list of the respective source
    :param source: source folder (see README)
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    :param index: starting file index number, 0 and 1 starts from the first file found in the folder
    :param limit: maximum number of files in reply list
    :return: list with file names
    """

    settings = {
        "source": source,  # source location: scheduler, web, etc...
        "index": index,  # start position of file index
        "limit": limit  # maximum number of files in reply structure
    }

    file_list = None

    api_url = f"http://{ip_address}/api/v1/files/list?key={key}"

    response = api_call(api_url, settings=settings, timeout=timeout)  # Query images in date/time range

    if response and response.status_code == 200:
        # command successful
        file_list = response.json()
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")

    return file_list


# startDateTime and endDateTime according to ISO8601
def get_files_in_range(start_datetime, end_datetime, source, ip_address=config.CAMERA_IP,
                       key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Get list of files that were created in a given time range
    :param start_datetime: Start date and time (according to ISO8601)
    :param end_datetime: End date and time (according to ISO8601)
    :param source: source folder (see README)
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    :return: list with file names
    """

    settings = {  # startDateTime and endDateTime according to ISO8601
        "startDateTime": start_datetime,
        "endDateTime": end_datetime,
        "source": source
    }

    files_in_range = None

    api_url = f"http://{ip_address}/api/v1/files/firstinrange?key={key}"

    response = api_call(api_url, settings=settings, timeout=timeout)  # Query first file in date/time range

    if response and response.status_code == 200:  # command successful
        files_in_range = response.json()
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")

    return files_in_range


def take_ms_image(ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY, timeout=120):
    """
    Takes multispectal image using the global settings
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    :return: file information (python dict)
    """
    file_list = None

    api_url = f"http://{ip_address}/api/v1/files/takeimage?key={key}"

    response = api_call(api_url, timeout=timeout)  # Take multispectral image

    if response and response.status_code == 200:
        # command successful
        file_list = response.json()

    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")

    return file_list


def take_mono_image(spectrum, brightness, exposure, filename,
                    ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Takes multispectal image using the global settings
    :param filename: name of the file the monochrome image should be written to (locally)
    :param exposure: time in seconds (see README)
    :param brightness: 0-1000
    :param spectrum: 0-10, see README
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    """

    settings = {
        "spectrum": spectrum,
        "brightness": brightness,
        "exposure": exposure
    }

    name, file_extension = os.path.splitext(filename)

    print("taking monochrome image")
    print(f"Settings: filename {filename}, spectrum {spectrum}, "
          f"brightness {brightness}, exposure {exposure}, IP {ip_address}")

    api_url = f"http://{ip_address}/api/v1/camera/image{file_extension}?key={key}"

    # get API response
    response = api_call(api_url, settings=settings, timeout=timeout)

    if response and response.status_code == 200:
        # command successful
        print("Store image to file")
        response = response.content  # get the image
        try:
            f = open(filename, "wb")  # save image to file
            f.write(response)
            f.close()
        except IOError:
            print("Write to file failed")
            exit(1)  # terminate, exit code 1
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")
        exit(1)  # terminate, exit code 1


def upload_file(file_path, ip_address=config.CAMERA_IP, key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Upload a file to the camera (e.g. config files)
    :param file_path: path to the file that should be uploaded
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    """

    filename = os.path.basename(file_path)

    # filename is part of the URL, wildcard is used on server side
    api_url = f"http://{ip_address}/api/v1/files/put/{filename}?key={key}"

    f = open(file_path, "rb")  # save image to file
    image = f.read()
    f.close()

    response = api_call(api_url, data=image, timeout=timeout)  # post file image
    if response and response.status_code == 200:
        print(f"Command succeeded, file {filename} uploaded")
    elif response:
        print(f"command failed, response code {response.status_code}, info: {response.content}")
    else:
        print("Command timeout")


def download_files(file_list, source, path=None, ip_address=config.CAMERA_IP,
                   key=config.UNIQUE_KEY, timeout=config.API_V1_TIMEOUT):
    """
    Download (multiple) files
    :param file_list: list with a single or multiple files that should be downloaded
    :param source: source folder (see README)
    :param path: local path the files should be downloaded to
    :param ip_address: IP address of the camera
    :param key: API key of the camera
    :param timeout: sets the timeout in seconds
    :return:
    """

    for file in file_list:
        print(f"Downloading {file}")
        image_file = get_file(filename=file, source=source,
                              ip_address=ip_address, key=key, timeout=timeout)

        if path is None:
            path = source

        os.makedirs(path, exist_ok=True)  # creates a folder named after the source to store the images

        if image_file:
            full_path = f"{path}/{file}"
            print(f"Storing file to {full_path}")
            try:
                f = open(full_path, "wb")  # save image to file
                f.write(image_file)
                f.close()
            except IOError:
                print("Write to file failed")
        else:
            print("No files to store")
