from machine import ADC, Pin, PWM
import utime
import network
from time import sleep, time
import urequests
import random

RED_PIN_NUMBER = 15    # Example: GP15
GREEN_PIN_NUMBER = 14  # Example: GP14
BLUE_PIN_NUMBER = 13   # Example: GP13

# Initialize ADC on GP26 (ADC0)
adc = ADC(Pin(26))
buzzer = Pin(17, Pin.OUT)
red_pin = PWM(Pin(RED_PIN_NUMBER, Pin.OUT))
green_pin = PWM(Pin(GREEN_PIN_NUMBER, Pin.OUT))
blue_pin = PWM(Pin(BLUE_PIN_NUMBER, Pin.OUT))

FREQUENCY = 440  # Frequency in Hz
red_pin.freq(FREQUENCY)
green_pin.freq(FREQUENCY)
blue_pin.freq(FREQUENCY)

def connect_wifi(ssid, password, timeout=10):
    """
    Connects to the specified Wi-Fi network.
    
    Args:
        ssid (str): The SSID of the Wi-Fi network.
        password (str): The password for the Wi-Fi network.
        timeout (int): Maximum time to wait for connection in seconds.
        
    Returns:
        bool: True if connected successfully, False otherwise.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    print('Connecting to Wi-Fi...', end='')
    
    start_time = time()
    while not wlan.isconnected():
        if time() - start_time > timeout:
            print("\nFailed to connect to Wi-Fi.")
            return False
        print('.', end='')
        sleep(1)
    
    print("\nConnected to Wi-Fi.")
    print('Network Config:', wlan.ifconfig())
    return True

def make_get_request(url):
    """
    Performs an HTTP GET request to the specified URL.
    
    Args:
        url (str): The URL to send the GET request to.
        
    Returns:
        dict: Parsed JSON response if successful, None otherwise.
    """
    try:
        response = urequests.get(url)
        print(f"GET {url} - Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response JSON:", data)
            response.close()
            return data
        else:
            print("Failed to retrieve data.")
            response.close()
            return None
    except Exception as e:
        print("An error occurred during GET request:", e)
        return None

SSID = "Neecathon"
PASSWORD = "neecathon2024!"
connect_wifi(SSID, PASSWORD)

def check_buzzer():
    GET_URL = "http://172.20.199.108:5000/check_buzzer_status"
    response = make_get_request(GET_URL)
    if response is None:
        return
    
    if response['buzzer_on']:
        play_buzzer()

def play_buzzer():
    buzzer.on()
    utime.sleep(0.5)
    buzzer.off()

def set_color(r, g, b):
    # Scale RGB values to PWM duty cycle (0-65535)
    red_duty = int((r / 255) * 65535)
    green_duty = int((g / 255) * 65535)
    blue_duty = int((b / 255) * 65535)
    
    red_pin.duty_u16(red_duty)
    green_pin.duty_u16(green_duty)
    blue_pin.duty_u16(blue_duty)


# Variables for signal processing
buffer_size = 50  # Buffer size for calculating the mean
values_buffer = [0] * buffer_size
buffer_index = 0

# Variables for heartbeat calculation
last_peak_time = 0
bpm = 0
peak_detected = False

# Threshold adjustment factor
threshold_factor = 1.15  # Adjust as needed

# Main loop
while True:
    # Read raw analog value from sensor
    raw_value = adc.read_u16()

    # Store raw value in buffer
    values_buffer[buffer_index] = raw_value
    buffer_index = (buffer_index + 1) % buffer_size

    # Calculate mean of the buffer
    mean_value = sum(values_buffer) / buffer_size

    # Define threshold as a factor above the mean
    threshold = mean_value * threshold_factor

    # Get current time in milliseconds
    current_time = utime.ticks_ms()

    # Peak detection logic
    if raw_value > threshold and not peak_detected:
        # Possible peak detected
        peak_detected = True
        # Debounce to avoid multiple detections within 300ms
        if utime.ticks_diff(current_time, last_peak_time) > 300:
            time_between_beats = utime.ticks_diff(current_time, last_peak_time)
            last_peak_time = current_time
            bpm = 60000 / time_between_beats
            print('Heartbeat detected. BPM:', int(bpm))

    elif raw_value < mean_value and peak_detected:
        # Peak has fallen below the mean, reset peak detection
        peak_detected = False

    # Optional: print raw and mean values for debugging
    # print('Raw:', raw_value, 'Mean:', mean_value, 'Threshold:', threshold)

    # Delay for 10ms to sample at 100Hz
    sleep(1)
    check_buzzer()

    # Generate 3 random integers
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    set_color(r,g,255)
