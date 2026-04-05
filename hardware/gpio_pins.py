"""
GPIO Pin Definitions and Hardware Setup
Defines the GPIO pins and hardware interface for the boiler alarm system.
"""

# Standard GPIO pin assignments for Raspberry Pi
class GPIOPins:
    """Standard GPIO pin definitions for the boiler alarm system."""
    
    # Default alarm input pin
    ALARM_INPUT = 18  # GPIO 18 (Physical pin 12)
    
    # Optional status LED pins
    STATUS_LED_GREEN = 16  # GPIO 16 (Physical pin 36) - System OK
    STATUS_LED_RED = 20    # GPIO 20 (Physical pin 38) - Alarm Active
    STATUS_LED_BLUE = 21   # GPIO 21 (Physical pin 40) - Network/Email status
    
    # Optional buzzer/relay output pins
    LOCAL_BUZZER = 26      # GPIO 26 (Physical pin 37) - Local alarm buzzer
    RELAY_OUTPUT = 19      # GPIO 19 (Physical pin 35) - External relay control

# Pin configuration constants
class PinConfig:
    """Pin configuration constants."""
    
    # Pull-up/down resistor configuration
    PULL_UP = True
    PULL_DOWN = False
    
    # Active state definitions
    ACTIVE_LOW = "LOW"
    ACTIVE_HIGH = "HIGH"
    
    # Timing constants (in seconds)
    DEBOUNCE_TIME = 2.0      # Minimum time alarm must be active before triggering
    CHECK_INTERVAL = 0.1     # How often to check GPIO pins
    LED_BLINK_RATE = 0.5     # Status LED blink rate

# Hardware specifications
HARDWARE_SPECS = {
    "raspberry_pi_models": [
        "Raspberry Pi 3 Model B+",
        "Raspberry Pi 4 Model B", 
        "Raspberry Pi Zero W",
        "Raspberry Pi Zero 2 W"
    ],
    "gpio_voltage": "3.3V",
    "max_current_per_pin": "16mA",
    "recommended_current": "8mA",
    "input_voltage_range": {
        "low": "0V - 0.8V",
        "high": "2.0V - 3.3V"
    }
}