# RAYN Vision Camera REST API v1 (Python-Agnostic Reference)

This document summarizes the REST endpoints exposed by the camera and inferred from this repository's API client.

Base URL pattern:

`http://<CAMERA_IP>/api/v1/<endpoint>?key=<API_KEY>`

Authentication:

- Query parameter `key` is required on all endpoints.

Transport notes:

- Most endpoints are called as HTTP `GET`.
- File upload uses HTTP `POST` with `Content-Type: application/octet-stream`.
- Requests in this repo send parameters as JSON payload on `GET` requests for endpoints that require inputs.

## 1) System Endpoints

### GET `/status`
Get basic camera status.

Typical response fields:

- camera name
- firmware version
- timestamp

### GET `/info`
Get camera info and health details.

Typical response fields:

- storage (e.g., SD card info)
- health/diagnostic values

### GET `/reset`
Trigger a camera restart.

Response:

- Success/failure status.

### GET `/flashlight`
Flash one LED spectrum channel for a duration.

Parameters:

- `spectrum` (int, `0..10`)
- `brightness` (int, `0..1000`)
- `time` (int, milliseconds)

Response:

- Echo/status JSON from device.

## 2) File Endpoints

### GET `/files/get`
Retrieve one file from camera storage.

Parameters:

- `filename` (string)
- `source` (string)

Response:

- Binary file content.

### GET `/files/delete`
Delete one file from camera storage.

Parameters:

- `filename` (string)
- `source` (string)

Response:

- Success/failure status.

### GET `/files/list`
List files from a source with pagination controls.

Parameters:

- `source` (string)
- `index` (int, start index; defaults to `0`)
- `limit` (int, max items; defaults to `500`)

Typical response shape:

- `files`: array of filenames
- `source`: source name
- `total`: total file count

### POST `/files/put/{filename}`
Upload a file (e.g., config file) to camera storage.

Path parameter:

- `filename` (string)

Body:

- Raw binary payload (`application/octet-stream`)

Response:

- Success/failure status.

## 3) Image Endpoints

### GET `/images/firstinrange`
Get files created in a datetime range.

Parameters:

- `startDateTime` (ISO8601 datetime string)
- `endDateTime` (ISO8601 datetime string)
- `source` (string)

Typical response shape:

- `files`: array of filenames
- source/time metadata (implementation-dependent)

### GET `/images/takeimage`
Capture a multispectral image set using camera global settings.

Parameters:

- None required by the client in this repository.

Typical response shape:

- `files`: array of generated filenames
- `source`: source folder name

### GET `/camera/image{ext}`
Capture a single monochrome image and return binary image data.

`{ext}` examples:

- `.jpg`
- `.png`

Parameters:

- `spectrum` (int, `0..10`)
- `brightness` (int, `0..1000`)
- `exposure` (float seconds, documented range `0.0..0.25`)

Response:

- Binary image bytes.

## 4) Source Values (from repository docs)

Known `source` values:

- `service` (log files)
- `config` (configuration files)
- `scheduler` (scheduler-captured images)
- `api_takeimages` (API-captured images)
- `io_takeimages` (IO-captured images)
- `web_image` (web UI-captured images)

## 5) Spectrum Index Values

- `0`: none
- `1`: blue (475 nm)
- `2`: cyan (500 nm)
- `3`: green (526 nm)
- `4`: amber (595 nm)
- `5`: red (630 nm)
- `6`: deep red (665 nm)
- `7`: far red (740 nm)
- `8`: NIR-850
- `9`: white (5700 K)
- `10`: NIR-940

## 6) Quick Examples (tool/language agnostic)

Status:

`GET http://<CAMERA_IP>/api/v1/status?key=<API_KEY>`

List scheduler images:

`GET http://<CAMERA_IP>/api/v1/files/list?key=<API_KEY>`

with body/params:

```json
{
  "source": "scheduler",
  "index": 0,
  "limit": 500
}
```

Take multispectral image:

`GET http://<CAMERA_IP>/api/v1/images/takeimage?key=<API_KEY>`

Download one file:

`GET http://<CAMERA_IP>/api/v1/files/get?key=<API_KEY>`

with body/params:

```json
{
  "filename": "example.jpg",
  "source": "api_takeimages"
}
```

Upload file:

`POST http://<CAMERA_IP>/api/v1/files/put/<filename>?key=<API_KEY>`

with raw binary payload.

## 7) Implementation Note

This reference is derived from:

- `api_v1.py`
- `README.md`

Device firmware may add/change fields or validation rules. Confirm against camera firmware release notes for strict integration contracts.
