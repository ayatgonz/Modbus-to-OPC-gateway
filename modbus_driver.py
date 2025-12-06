from pymodbus.client import ModbusTcpClient

# ================= CONFIGURATION =================
# REPLACE THIS with your Ubuntu PC's IP Address!
SERVER_IP = "172.16.10.5" 
SERVER_PORT = 5020
# =================================================

def get_system_metrics():
    """
    Reads the 10 System Sensor registers (0-9) from Ubuntu.
    Returns a list: [CPU, RAM, DISK, FREQ, PROCS, BATT%, CHARGE, SWAP, CORE1, CORE2]
    """
    client = ModbusTcpClient(SERVER_IP, port=SERVER_PORT)
    
    try:
        if not client.connect():
            return None

        # Read 10 registers starting at address 0
        rr = client.read_holding_registers(address=0, count=10, slave=1)
        
        if rr.isError():
            print(f" Read Error: {rr}")
            return None
            
        return rr.registers

    except Exception as e:
        print(f" Connection Error: {e}")
        return None
    finally:
        client.close()

def write_setpoint(offset, value):
    """
    Writes a value to the Setpoint registers (10-12).
    offset 0 -> Register 10
    offset 1 -> Register 11
    offset 2 -> Register 12
    """
    client = ModbusTcpClient(SERVER_IP, port=SERVER_PORT)
    target_register = 10 + offset # Map 0-2 to 10-12

    try:
        if not client.connect():
            return False

        # Write single register
        result = client.write_register(address=target_register, value=value, slave=1)
        
        if result.isError():
            print(f" Write Error: {result}")
            return False
            
        return True

    except Exception as e:
        print(f" Write Exception: {e}")
        return False
    finally:
        client.close()

# --- Testing Block ---
if __name__ == "__main__":
    print(" Testing Modbus Driver...")
    data = get_system_metrics()
    if data:
        print(f" Received: {data}")
    else:
        print(" Failed to connect to Ubuntu Server.")
