import asyncio
import logging
from asyncua import Server, ua

# --- IMPORT DRIVERS ---
import modbus_driver       
import sensehat_driver     

# CONFIGURATION
OPC_IP = "172.16.0.199"
OPC_PORT = 4840

class SubscriptionHandler:
    """
    Handles writes coming FROM OPC TO Raspberry Pi
    """
    def datachange_notification(self, node, val, data):
    
        node_name = node.nodeid.Identifier
        
        print(f" {val} to {node_name}")
        
        # Route writes to Modbus Driver
        if node_name == "Setpoint_A":
            modbus_driver.write_setpoint(0, val) # Writes to Reg 10
        elif node_name == "Setpoint_B":
            modbus_driver.write_setpoint(1, val) # Writes to Reg 11
        elif node_name == "Setpoint_C":
            modbus_driver.write_setpoint(2, val) # Writes to Reg 12

async def main():
    # --- 1. Setup OPC UA Server ---
    server = Server()
    await server.init()
    server.set_endpoint(f"opc.tcp://{OPC_IP}:{OPC_PORT}/freeopcua/server/")
    
    # Register Namespace
    uri = "http://raspberrypi.gateway"
    idx = await server.register_namespace(uri)

    # ==================================================
    #FOLDER 1: ------ Object Oriented Data in OPC UA Directory ---------------- 
    # ==================================================
    ubuntu_folder = await server.nodes.objects.add_object(idx, "Ubuntu_System")

    # Create Sensor Tags (Read Only)
    tag_cpu      = await ubuntu_folder.add_variable(idx, "CPU_Usage", 0)
    tag_ram      = await ubuntu_folder.add_variable(idx, "RAM_Usage", 0)
    tag_disk     = await ubuntu_folder.add_variable(idx, "Disk_Usage", 0)
    tag_freq     = await ubuntu_folder.add_variable(idx, "CPU_Freq_MHz", 0)
    tag_procs    = await ubuntu_folder.add_variable(idx, "Process_Count", 0)
    tag_batt     = await ubuntu_folder.add_variable(idx, "Battery_Percent", 0)
    tag_charging = await ubuntu_folder.add_variable(idx, "Is_Charging", 0)
    tag_swap     = await ubuntu_folder.add_variable(idx, "Swap_Usage", 0)
    tag_core1    = await ubuntu_folder.add_variable(idx, "Core_1_Load", 0)
    tag_core2    = await ubuntu_folder.add_variable(idx, "Core_2_Load", 0)

    # Create Setpoint Tags (Writable)
    # Note: The second argument "Setpoint_A" becomes the Identifier we check above
    sp_a = await ubuntu_folder.add_variable(idx, "Setpoint_A", 0)
    sp_b = await ubuntu_folder.add_variable(idx, "Setpoint_B", 0)
    sp_c = await ubuntu_folder.add_variable(idx, "Setpoint_C", 0)

    # Allow Ignition to write to Setpoints
    await sp_a.set_writable()
    await sp_b.set_writable()
    await sp_c.set_writable()

    # ==================================================
    #FOLDER 2: ------ Object Oriented Data in OPC UA Directory ---------------- 
    # ==================================================
    sense_folder = await server.nodes.objects.add_object(idx, "SenseHAT_Data")
    
    # Create Sense HAT Tags
    tag_temp  = await sense_folder.add_variable(idx, "Temperature_C", 0.0)
    tag_hum   = await sense_folder.add_variable(idx, "Humidity_Pct", 0.0)
    tag_pres  = await sense_folder.add_variable(idx, "Pressure_mbar", 0.0)
    tag_pitch = await sense_folder.add_variable(idx, "Pitch", 0.0)
    tag_roll  = await sense_folder.add_variable(idx, "Roll", 0.0)

    # --- 2. Setup Subscription (Listen for Ignition Writes) ---
    handler = SubscriptionHandler()
    sub = await server.create_subscription(500, handler)
    await sub.subscribe_data_change(sp_a)
    await sub.subscribe_data_change(sp_b)
    await sub.subscribe_data_change(sp_c)

    print(f"Gateway Running on {OPC_IP}:{OPC_PORT}")

    async with server:
        while True:
            # --- TASK A: Update Ubuntu Data (Modbus) ---
            mb_data = modbus_driver.get_system_metrics()
            
            if mb_data:
                await tag_cpu.write_value(mb_data[0])
                await tag_ram.write_value(mb_data[1])
                await tag_disk.write_value(mb_data[2])
                await tag_freq.write_value(mb_data[3])
                await tag_procs.write_value(mb_data[4])
                await tag_batt.write_value(mb_data[5])
                await tag_charging.write_value(mb_data[6])
                await tag_swap.write_value(mb_data[7])
                await tag_core1.write_value(mb_data[8])
                await tag_core2.write_value(mb_data[9])
            else:
                print("Ubuntu Server Offline")

            # --- TASK B: Update Sense HAT Data (Local) ---
            env = sensehat_driver.get_env_data()     # [Temp, Hum, Pres]
            ori = sensehat_driver.get_orientation()  # [Pitch, Roll, Yaw]
            
            await tag_temp.write_value(env[0])
            await tag_hum.write_value(env[1])
            await tag_pres.write_value(env[2])
            await tag_pitch.write_value(ori[0])
            await tag_roll.write_value(ori[1])

            # Wait 2 seconds
            await asyncio.sleep(2)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGateway Stopped.")
