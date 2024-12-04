# Copyright 2024 ETC Inc d/b/a RAYN Growing Systems
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

import api_v1
import sys

# default parameters
spectrum = 0  # spectrum 0
brightness = 0  # LEDs off
exposure = 0.0  # exposure in 0.3s
filename = "image.jpg"  # default filename and default JPG


if __name__ == "__main__":
    n = len(sys.argv)  # check number of arguments TODO change argument parsing and add help

    for i in range(1, n, 2):  # check for command line arguments
        if sys.argv[i] == "spectrum":  # spectrum 0 - 10, 0 is dark
            spectrum = sys.argv[i + 1]
        elif sys.argv[i] == "brightness":  # LED brightness range 0- 1000
            brightness = sys.argv[i + 1]
        elif sys.argv[i] == "filename":  # optional filename to save to
            filename = sys.argv[i + 1]
        elif sys.argv[i] == "exposure":  # exposure time rang 0.0 - 0.25
            exposure = sys.argv[i + 1]
        elif sys.argv[i] == "ip":  # IP Address
            ip_address = sys.argv[i + 1]
        else:  # check for invalid arguments
            print("argument unknown: " + sys.argv[i])

    api_v1.take_mono_image(spectrum=spectrum, brightness=brightness, exposure=exposure, filename=filename)
