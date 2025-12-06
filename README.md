# Modbus-to-OPC-gateway
Python-based IIoT gateway Modbus to OPC UA with Raspberry Pi

-- Function  --

It serve data via modbus register.
It also listen for remote setpoints from the Gateway.

-- Dependencies --

1. Python 3.7+ required.
2. Install dependencies ('pymodbus' must be version 3.6.9)
3. psutil lib (if you are going to use OS system data)

--Script Configuration-- 

Look for the CONFIGURATION block near the top:

SERVER_IP = "X.X.X.X"   <-- Set the Server IP address, must match with the current IP address of the device's NIC
SERVER_PORT = XXXXX      <-- Standard Modbus is 502. Can be configured with any port, avoid the use of standard port number of other protocols.

-- Create your own DataSet --
It is possible to use this modbus server to provide any dataset:

STEP 1: Edit 'system_sensors.py' (if necessary)

   1. Go to the 'get_live_metrics()' function.
   
   2. Erase all the function or edit as necessary, write your logic here.
   
   3. Edit the return [data1, data2, data3...] to provide your own variables

****NOTE: The current address ModbusSequentialDataBlock is fixed to 100 registers and 3 holding register for writting.
          If more variables are requiered please follow STEP 2.


STEP 2: Edit 'modbus_app.py'
   1. The update_loop() function automatically writes the whole list to Modbus.
   
   2. Ensure the list length does not exceed the register block size currently set at 100 register.
   
   	2.a) If more than 100 variables is requiered edit this line of code --->> 'hr=ModbusSequentialDataBlock(0, [0] * 100)' Replace 100 to any number that not exceed 65535  
 	     (Recommendation less than 123 due to networks package limitation).
 	     
 	2.b) Also edit the line of code -->> 'current_values = slave_context.getValues(3, 10, 3)', where the 10 should be greater than your 
 	     'get_live_metrics()'return list to avoid data overlap and edit the second 3 to expand the number of holding register to be writting.
 	     
 	     ****NOTE: 'current_values = slave_context.getValues(3, 10, 3)' in this expression the first 3 is for the modbus register type.
 	    	        3 is for holding register 'slave_context.getValues(regtype,addres,nregisters)' check modbus standard and pymodbus documentation if other type of register is 
 	    	        required
   	
   3. Ensure that 'modbus_app.py' and 'system_sensors.py' are in the same directory and just 'modbus_app.py'. The script 'system_sensors.py' is inside the dependancies of 
      'modbus_app.py'. 'system_sensor.py' not required to be executed.
  
 
