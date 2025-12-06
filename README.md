# Modbus-to-OPC-gateway
Python-based IIoT gateway Modbus to OPC UA with Raspberry Pi

A IIoT Edge Gateway project that uses a Raspberry Pi to bridge legacy Modbus TCP data and local sensors into a unified OPC UA stream for SCADA Systems.

An Ubuntu host acts as a Modbus Server, collecting system metrics from OS using psutil lib and provide a modbus server for this OS data. A Raspberry Pi Gateway polls this data via modbus, aggregates it with local Sense HAT environmental readings, and exposes the unified information model via an OPC UA Server for real-time SCADA monitoring and bidirectional setpoint control.

This project is divided in two projects:
1.Modbus_Server: This branch acts as the data producer or "Virtual PLC." It runs an asynchronous Modbus TCP server that collects real-time system metrics (CPU, RAM) to simulate industrial sensor outputs.
Documentation: Includes a README_Server.md with instructions on how to modify the collector script to broadcast any custom data (APIs, databases, or files) instead of system metrics.

2. Modbus_Client-to-OPC-UA (Raspberry Pi): This branch functions as the protocol bridge. It acts as a Modbus Client to poll the server, aggregates that data with local Sense HAT sensor readings, and publishes the unified dataset via a secure OPC UA Server for SCADA control.
Documentation: Includes a README.md with instructions on how to configure network IPs and map any custom Modbus registers to new OPC UA tags.

-- INSTRUCTIONS --

----Modbus Server----

Step 1: Download the Modbus_Server scripts 'system_sensor.py' and 'modbus_app' in the Modbus server PC.
Step 2: Follow the networks config and customization steps as requiered in the Modbus_Server readme.md file

----Modbus_Client-to-OPC-UA----

Step 1: Download the Modbus_Server scripts 'modbus_driver.py', 'sensehat_driver.py' and 'opcua_gateway.py' in the Edge Computing (Raspberry Pi).
Step 2: Follow the networks config and customization steps as requiered in the Modbus_Client-to-OPC-UA readme.md file

****NOTE: the sense hat hardware is requeried, if do not use a sensehat you can remove the 'sensehat_driver.py', and perform the steps in the Modbus_Client-to-OPC-UA readme.md file
