import os
import platform

def get_cpu_usage():
    if platform.system() == "Windows":
        return os.popen('wmic cpu get loadpercentage').read().strip()
    elif platform.system() == "Linux":
        return os.popen("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").read().strip()
    elif platform.system() == "Darwin":
        return os.popen("ps -A -o %cpu | awk '{s+=$1} END {print s}'").read().strip()
    else:
        return "Unsupported platform"

def get_memory_usage():
    if platform.system() == "Windows":
        return os.popen('wmic OS get FreePhysicalMemory /Value').read().strip()
    elif platform.system() == "Linux":
        return os.popen("free | awk '/Mem:/ {print $3/$2 * 100.0}'").read().strip()
    elif platform.system() == "Darwin":
        return os.popen("ps -A -o %mem | awk '{s+=$1} END {print s}'").read().strip()
    else:
        return "Unsupported platform"

def hash_float(value):
    # Hash function to map any value to a float between 0 and 1
    return (hash(str(value)) % 1000000) / 1000000.0

def measure_randomness(lower_bound, upper_bound):
    cpu_usage = float(get_cpu_usage())
    memory_usage = float(get_memory_usage())
    random_coeff = hash_float(cpu_usage * memory_usage)
    
    # Use modulo to ensure the generated number is within the specified bounds
    number_range = upper_bound - lower_bound
    number = lower_bound + (random_coeff * number_range) % number_range
 
    return number

if __name__ == "__main__":
    user_input_lower_limit = float(input("Lower bound: "))
    user_input_upper_limit = float(input("Upper bound: "))
    
    random_number = round(measure_randomness(user_input_lower_limit, user_input_upper_limit))
    print(random_number)
