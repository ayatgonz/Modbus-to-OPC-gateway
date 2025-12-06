from sense_hat import SenseHat

# Initialize hardware once when the script loads
try:
    sense = SenseHat()
    sense.clear() # Clear the LED matrix
except Exception as e:
    print(f"Sense HAT not found: {e}")
    sense = None

def get_env_data():
    """
    Reads Temperature, Humidity, and Pressure.
    Returns: [Temp_C, Humidity_%, Pressure_mbar]
    """
    if not sense:
        return [0.0, 0.0, 0.0]

    try:
        # Get sensors
        temp = round(sense.get_temperature(), 2)
        hum  = round(sense.get_humidity(), 2)
        pres = round(sense.get_pressure(), 2)
        
        return [temp, hum, pres]
    except Exception as e:
        print(f"Sensor Read Error: {e}")
        return [0.0, 0.0, 0.0]

def get_orientation():
    """
    Reads the gyroscope/accelerometer.
    Returns: [Pitch, Roll, Yaw]
    """
    if not sense:
        return [0.0, 0.0, 0.0]
        
    try:
        o = sense.get_orientation()
        pitch = round(o["pitch"], 2)
        roll  = round(o["roll"], 2)
        yaw   = round(o["yaw"], 2)
        
        return [pitch, roll, yaw]
    except:
        return [0.0, 0.0, 0.0]

# --- Testing Block ---
if __name__ == "__main__":
    import time
    print("Testing Sense HAT...")
    while True:
        env = get_env_data()
        ori = get_orientation()
        print(f"🌡️ Env: {env} | Gyro: {ori}")
        time.sleep(1)
