import pyshark

# Function to extract RSSI from text data
def extract_rssi_from_text_data(text_data):
    lines = text_data.split('\n')
    rssi = None

    for line in lines:
        if "RSSI:" in line:
            rssi_str = line.strip()
            rssi = int(rssi_str.split(" ")[1])  # Extract the numeric part of RSSI
            break

    return rssi

# Function to extract Data from text data
def extract_data_from_text_data(text_data):
    lines = text_data.split('\n')
    data = None

    for line in lines:
        if "Data:" in line:
            data = line.strip().replace("Data:", "").strip()
            break

    return data

# Function to extract Power Level from text data
def extract_power_level_from_text_data(text_data):
    lines = text_data.split('\n')
    power_level = None

    for line in lines:
        if "Power Level (dBm):" in line:
            power_level_str = line.strip()
            power_level = int(power_level_str.split(" ")[3])
            break

    return power_level

# Function to extract advertising address from text data
def extract_macAdd_from_text_data(text_data):
    lines = text_data.split('\n')
    macAdd = None

    for line in lines:
        if "Advertising Address: " in line:
            macAdd = line.strip().replace("Advertising Address:", "").strip()
            break

    return macAdd
# Capture packets using pyshark
cap = pyshark.FileCapture('/Users/nickmuratore/Downloads/1hrBLECAP.pcapng')

# Extract the first and second packets or any based on index
first_packet = str(cap[1])
second_packet = str(cap[2])

# Write the first and second packets to text files
with open('pysharkFlags0.txt', 'w') as file:
    file.write(first_packet)

with open('pysharkFlags1.txt', 'w') as file:
    file.write(second_packet)

# Get the text data for both captures
with open('pysharkFlags0.txt', 'r') as file:
    text_data_0 = file.read()

with open('pysharkFlags1.txt', 'r') as file:
    text_data_1 = file.read()

# Extract RSSI from the text data
rssi_0 = extract_rssi_from_text_data(text_data_0)
rssi_1 = extract_rssi_from_text_data(text_data_1)

# Extract Data from the text data
data_0 = extract_data_from_text_data(text_data_0)
data_1 = extract_data_from_text_data(text_data_1)

# Extract Power Level from the text data
power_level_0 = extract_power_level_from_text_data(text_data_0)
power_level_1 = extract_power_level_from_text_data(text_data_1)

# Define the RSSI threshold for similarity
rssi_threshold = 10  # You can adjust this threshold as needed

# Define power level ranges for classification
phone_power_level_range = (10, 12)
smart_watch_power_level_range = (7, 9)

#Extract advertising address from text data
macAdd_0 = extract_macAdd_from_text_data(text_data_0)
macAdd_1 = extract_macAdd_from_text_data(text_data_1)

# Print the RSSI, Power Level (if available), and Data for both captures
print("Packet A:")
print(f"Advertising Address: {macAdd_0}")
print(f"RSSI: {rssi_0}")
if power_level_0 is not None:
    print(f"Power Level: {power_level_0} dBm")
    if phone_power_level_range[0] <= power_level_0 <= phone_power_level_range[1]:
        print("Device: Phone")
    elif smart_watch_power_level_range[0] <= power_level_0 <= smart_watch_power_level_range[1]:
        print("Device: Smart Watch")
    else:
        print("Device: Unknown")
else:
    print("Power Level: Not available")
print(f"Data: {data_0}")

print("Packet B:")
print(f"Advertising Address: {macAdd_1}")
print(f"RSSI: {rssi_1}")
if power_level_1 is not None:
    print(f"Power Level: {power_level_1} dBm")
    if phone_power_level_range[0] <= power_level_1 <= phone_power_level_range[1]:
        print("Device: Smart Phone")
    elif smart_watch_power_level_range[0] <= power_level_1 <= smart_watch_power_level_range[1]:
        print("Device: Smart Watch")
    else:
        print("Device: Unknown")
else:
    print("Power Level: Not available")
print(f"Data: {data_1}")

# Compare RSSI, Power Level, and Data values and declare if they are from the same device
if (
    abs(rssi_0 - rssi_1) <= rssi_threshold
    and data_0[:5] == data_1[:5]  # Check if the first 5 characters match
    and (
        (power_level_0 is None and power_level_1 is None)  # Check if both power levels are not available
        or (
            power_level_0 is not None
            and power_level_1 is not None
            and (
                phone_power_level_range[0] <= power_level_0 <= phone_power_level_range[1]
                or smart_watch_power_level_range[0] <= power_level_0 <= smart_watch_power_level_range[1]
            )
            and (
                phone_power_level_range[0] <= power_level_1 <= phone_power_level_range[1]
                or smart_watch_power_level_range[0] <= power_level_1 <= smart_watch_power_level_range[1]
            )
        )
    )
):
    print("These are the same device.")
else:
    print("These are different devices.")
