import psutil

def get_live_metrics():
    """
    Returns a list of 10 integers representing the system health.
    Format: [CPU, RAM, DISK, FREQ, PROCS, BATT%, CHARGE, SWAP, CORE1, CORE2]
    
    YOU CAN ERASE THE WHOLE FUNCTION TO PROVIDE YOUR OWN DATASET
    """
    # 1. Basic Stats
    cpu = int(psutil.cpu_percent(interval=None))
    ram = int(psutil.virtual_memory().percent)
    disk = int(psutil.disk_usage('/').percent)
    freq = int(psutil.cpu_freq().current) if psutil.cpu_freq() else 0
    procs = len(psutil.pids())

    # 2. Battery Stats
    batt = psutil.sensors_battery()
    if batt:
        batt_pct = int(batt.percent)
        charging = 1 if batt.power_plugged else 0
    else:
        batt_pct = 0
        charging = 0

    
    swap = int(psutil.swap_memory().percent)
    
    
    cores = psutil.cpu_percent(interval=None, percpu=True)
    core1 = int(cores[0]) if len(cores) > 0 else 0
    core2 = int(cores[1]) if len(cores) > 1 else 0

    
    return [cpu, ram, disk, freq, procs, batt_pct, charging, swap, core1, core2]


if __name__ == "__main__":
    import time
    print("Data Reading")
    while True:
        data = get_live_metrics()
        print(f"Readings: {data}")
        time.sleep(1)
