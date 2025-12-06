# Modbus-to-OPC-gateway
Python-based IIoT gateway Modbus to OPC UA with Raspberry Pi

-- Function  --

It serve data via modbus register.
It also listen for remote setpoints from the Gateway.

-- Dependencies --

1. Python 3.7+
2. asyncua==1.1.0
3. pymodbus==3.6.9
3. sense-hat (Optional if sensehat hardware is be used)

--Script Configuration-- 

---------- MODBUS CLIENT ---------------
By default, the script reads 10 registers starting at 0. Can be adapted to any number of register arragement.

Step 1: Open 'modbus_driver.py'.

Step 2: Locate the 'get_system_metrics()' function.

Step 3: Modify the reading parameter 'rr = client.read_holding_registers(address=0, count=10, slave=1)' to match your Modbus Server modbus map
   - 'address': The start address from 0 up to 65535.
   - 'count':   How many consecutive registers to read (Max ~120 per call due to network package limitation).
   - 'slave':   The Unit ID of the device (usually 1, sometimes 0 or 255). (Used for Modbus RTU, ID=1 for TCP/IP)

Step 4: Modify the write logic if needed in 'write_setpoint()'.

---------- OPC UA GATEWAY ---------------
To add a new variable (Tag) that Ignition can see, you must edit 'opcua_gateway.py'.

Step 5: Add or remove local dependancies.

Step 6: Look for the section marked: "# ================= FOLDER 1 ..."

Step 7: Customize your OPC UA server, removing, editing or adding variables using the following Syntax:
        var_name = await folder_obj.add_variable(idx, "Displayed_Name", INITIAL_VALUE)
        ****NOTE: Currently the script use 'ubuntu_folder = await server.nodes.objects.add_object(idx, "Ubuntu_System")'. it can be edited to customize your own object.
	          You can remove, edit or add currents server.nodes.objects.add_object

Step 8: Look for the section marked: "# TASK A ..."

Step 9: link your new tag to a Modbus Register index using the following Syntax:
        await tag_name.write_value(mb_data[REGISTER_INDEX])

If you want to WRITE data to the Pi, follow these steps:

Step 10: Define tag inside 'async def main'. Create the variable and EXPLICITLY make it writable with the following Syntax:
  var_name = await folder_obj.add_variable(idx, "Displayed_Name", INITIAL_VALUE)
   ENSURING MAKE IT Wrtable --> await var_name.set_writable()

Step 11: Subscribe tags Inside 'async def main'
   await sub.subscribe_data_change(var_name)

  
