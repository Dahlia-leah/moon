# Device Connection Management

## Overview

This Odoo 17 module enables managing device connections like scales, with support for both USB and web-based connections. It can detect devices, read data (e.g., weight readings from a scale), and validate data format.

### Features:
- Detect USB devices (Linux, Windows, Mac).
- Fetch and validate scale data.
- Track connection status (`valid` or `invalid`).
- Handle scale data in a JSON format.


## Model Flow

1. **Device Creation**:
   - Create a record in the `devices.device` model to represent the physical device (e.g., a scale).

2. **Connection Management**:
   - Set up connections in the `devices.connection` model, linking them to the device. Each connection specifies a unique interaction method (e.g., USB or web-based).

3. **Data Handling**:
   - Fetch data from the device through the connection and store it in JSON format. Validate the data to ensure it adheres to the expected structure.

4. **Status Tracking**:
   - Automatically update the connection's status (`valid` or `invalid`) based on data validation results, helping users identify and resolve issues.

5. **Archiving/Deleting**:
   - Archive unused connections or delete them if they are not linked to any stock moves.

## Who Uses It?

- **Warehouse Managers**:
  - Manage scales for weighing inventory items.
  - Validate and monitor device connections to ensure accurate data collection.

- **System Administrators**:
  - Configure devices and connections during setup.
  - Troubleshoot connection issues and ensure all dependencies are installed.

## How to Use It?

1. **Setup**:
   - Install the module and required dependencies (`pyserial`, `requests`).

2. **Device Configuration**:
   - Navigate to **Devices** → **Devices** and create a record for the physical device.

3. **Create Connections**:
   - Go to **Devices** → **Device Connections** and add a new connection for the device.

4. **Fetch Data**:
   - Use the **Read Scale** action to retrieve and validate data from the device.

5. **Monitor Status**:
   - Regularly check the connection status (`valid` or `invalid`) to ensure proper operation.

6. **Archive/Delete**:
   - Archive inactive connections or delete unused ones (if not linked to stock moves).

## Models

### `devices.connection`

- **name**: Name of the connection (required).
- **device_id**: Related device (e.g., scale).
- **connection_code**: Unique connection code (for web-based connections).
- **url**: Computed URL for web-based connections.
- **json_data**: Stores JSON data fetched from the scale.
- **status**: Tracks the connection status (`valid` or `invalid`).
- **active**: Boolean flag for active status.
- **last_checked**: Timestamp of the last check.

## Key Functions

### 1. **Detect USB Devices**
   - Action to read and list all USB devices connected to the machine.

### 2. **Read Scale Data**
   - Action to read data from a connected scale via USB. Data is expected in the format:
     ```json
     {
         "unit": "g",
         "weight": 2046.0
     }
     ```

### 3. **Cron Job for Validation**
   - Periodically checks and validates the connection’s JSON data.

### 4. **Connection Validation**
   - If data is valid, the connection status is set to `valid`.
   - If the data is malformed, the status is set to `invalid`.

## Example Data

**Valid**:
```json
{
    "unit": "g",
    "weight": 2046.0
}
```

**Invalid**:
```json
{
    "error": "Invalid or no data received from scale."
}
```

## Usage

1. **Create Connection**: Navigate to **Devices** → **Device Connections**, then click **Create**.
2. **Read Scale Data**: After creating a connection, click **Read Scale** to fetch data.
3. **Archive/Delete Connections**: Use the **Archive Connection** and **Delete Connection** actions.

## Troubleshooting

- **Invalid Connection**: Ensure the correct device is connected or check the connection code.
- **Invalid JSON**: Make sure the scale outputs data in the correct format.

