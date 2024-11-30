from machine import ADC, Pin
import utime

# Initialize ADC on GP26 (ADC0)
adc = ADC(Pin(26))

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
    utime.sleep(0.01)
