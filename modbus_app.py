import asyncio
import logging
import system_sensors  
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext


SERVER_IP = "172.16.10.5"
SERVER_PORT = 5020

# Setup Logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

async def update_loop(context):
    """
    Task: Get data from the 'system_sensors' script and update Modbus
    """
    print("Sensor Started")
    while True:
        # 1. CALL THE OTHER SCRIPT TO GET DATA
        # We don't need to know how psutil works here. We just ask for the list.
        new_data = system_sensors.get_live_metrics()
        
        # 2. Update Registers 0-9
        slave_context = context[0]
        slave_context.setValues(3, 0, new_data)
        
        # print(f"updated: {new_data}") # Uncomment for debug
        await asyncio.sleep(2)

async def setpoint_loop(context):
    """
    Task: Watch Registers 10-12 for write commands
    """
    print("Setpoint Monitor Started")
    slave_context = context[0]
    last_values = [0, 0, 0]

    while True:
        # Check Registers 10, 11, 12
        current_values = slave_context.getValues(3, 10, 3)

        if current_values != last_values:
            print(f" NEW SETPOINTS: {current_values}")
            last_values = list(current_values)

        await asyncio.sleep(0.5)

async def run_server():
    # Initialize 100 Registers
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0] * 100)
    )
    context = ModbusServerContext(slaves=store, single=True)

    # Start Background Tasks
    asyncio.create_task(update_loop(context))
    asyncio.create_task(setpoint_loop(context))

    print(f"Modbus Server Running on {SERVER_IP}:{SERVER_PORT}")
    await StartAsyncTcpServer(context=context, address=(SERVER_IP, SERVER_PORT))

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nServer Stopped.")
