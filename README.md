![RAYN Vision System Camera](https://rayngrowingsystems.com/wp-content/uploads/2024/04/RAYN_VisionCamera_1160x200.jpg)

# RAYN Vision System Camera API v1
## Introduction
The RAYN Vision System (RVS) is a compact, multispectral camera imaging tool for plant researchers. 
The Vision Camera takes multispectral images for studying plant behavior. More information is available on the
[RAYN Website](https://rayngrowingsystems.com/products/rayn-vision-camera/).

The REST API and the respective python functions documented here 
allow to connect the camera to third party developer tools and analysis pipelines.

## Basics
API base URL: http://IP_ADRESS/api/v1/COMMAND?key=KEY

general commands:
- status: status/,
- info: info/
- reset: reset/
- flash up light: flashlight/
files:
- get file: files/get/
- delete file: files/delete/
- list all files: files/list/
images:
- list images in datetime range: images/firstinrange/
- take ms image: images/takeimage/

See function api_call() in api_v1.py for more information.

## Usage
The python module (api_v1.py) contains all relevant function to interact with the RVS Camera via the REST API (see examples).

Optional: Create a config.py file which contains defaults of the following settings: 
IP address, API key, API url, timeout duration (see config_example.py)

**Terminal commands**

Main command (Take monochrome image with default settings and saves it locally)

`python3 camera.py` 

Available settings: spectrum, brightness, exposure, filename, ip (see settings below)

Example: Take monochrome image with settings adjusted

`python3 camera.py spectrum 4 brightness 100 exposure 0.3 filename test.png ip 10.1.2.1`


## Settings
Depending on the call/command, additional settings are required (see respective functions).

Below the different settings are listed

### Brightness
Integer in the range from 0 to 1000

### Exposure time
Float in the range from 0.0 - 0.25 (seconds)

### Available spectra
| index | spectrum | main wavelength band |
|-------|----------|----------------------|
| 0     | none     | none                 |
| 1     | blue     | 475 nm               |
| 2     | cyan     | 500 nm               |
| 3     | green    | 526 nm               |
| 4     | amber    | 595 nm               |
| 5     | red      | 630 nm               |
| 6     | deep red | 665 nm               |
| 7     | far red  | 740 nm               |
| 8     | NIR-850  | 850 nm               |
| 9     | White    | 5700 K               |
| 10    | NIR-940  | 940 nm               |

### Available sources

| source        | comment                        |
|---------------|--------------------------------|
| service       | log files                      |
| config        | config files                   |
| scheduler     | images taken by the scheduler  |
| api_takeimage | images taken via API           |
| io_takeimage  | images taken via IO            |
| web_image     | images taken via web interface |

## Feedback and Comments

If you experience any problems or have feedback on the API/code, please add an issue to this repository or contact
[Alexander Kutschera](mailto:alexander.kutschera@etcconnect.com).

## License and Copyright

Copyright 2024 RAYN Growing Systems, Licensed under the Apache License, Version 2.0
