# Boiler Alarm Monitoring System - Hardware Wiring Guide

## Required Components

### Core Components
- **Raspberry Pi 3 Model B/B+** (perfect for boiler monitoring - recommended!)
- Raspberry Pi 4 Model B (overkill but works if you have one)
- Raspberry Pi Zero W/2W (budget option for simple installations)
- MicroSD card (16GB minimum, Class 10)
- **5V 2A power supply** for Pi 3 (5V 2.5A for Pi 4)
- Ethernet cable or WiFi connection

## Why Raspberry Pi 3 is Perfect for This Application

### **Pi 3 Specifications vs Requirements:**

| Feature | Pi 3 Capability | Boiler Monitor Needs | Result |
|---------|-----------------|---------------------|---------|
| **CPU** | 1.2GHz Quad-core | Single GPIO monitoring | ✅ **Massive Overkill** |
| **RAM** | 1GB | ~50MB Python app | ✅ **20x More Than Needed** |
| **GPIO** | 40 pins | 1 pin for alarm input | ✅ **39 Pins to Spare** |
| **Network** | WiFi + Ethernet | Email sending | ✅ **Perfect** |
| **Power** | 2A @ 5V | Low power monitoring | ✅ **Very Efficient** |
| **Reliability** | Industrial proven | 24/7 operation | ✅ **Excellent** |

### **Pi 3 Advantages for Boiler Monitoring:**
✅ **More than sufficient processing power** - could monitor 100+ sensors  
✅ **Excellent network connectivity** - reliable email sending  
✅ **Proven reliability** - thousands in industrial use  
✅ **Low cost** - often available used for $20-30  
✅ **Great GPIO support** - mature software ecosystem  
✅ **Cool running** - no cooling needed for this application

### Electrical Components

**For Permanent Installation:**
- **Perfboard/stripboard** or small PCB for permanent mounting
- **Wire nuts** or **terminal blocks** for secure connections
- **22-24 AWG stranded wire** for connections
- **Heat shrink tubing** for insulation

**For Testing/Prototyping Only:**
- Breadboard (temporary testing only)
- Jumper wires (male-to-female, male-to-male)

**Electronic Components:**
- 10kΩ pull-up resistors for GPIO pins
- **1kΩ current limiting resistors** for 12-24V optocoupler inputs
- **Optocoupler** for electrical isolation (REQUIRED for 12-24V):
  - **PC817** (recommended) - 5kV isolation, 50mA max LED current
  - **4N35** - 7.5kV isolation, 60mA max LED current  
  - **EL817** - 5kV isolation, 50mA max LED current
  - **6N137** - High-speed option if needed
- Status LEDs (optional):
  - Green LED - System OK
  - Red LED - Alarm Active
  - Blue LED - Network/Email Status
- 220Ω current limiting resistors for LEDs
- Local buzzer (optional, 5V active buzzer)
- **Multimeter** for voltage verification and testing
- **Small project enclosure** (IP65 rated for harsh environments)
- **Cable glands** for wire entry into enclosure

## Optocoupler Selection Guide

### Recommended Optocouplers for 12-24V Boiler Alarms

| Model | Package | Isolation | Max LED Current | Forward Voltage | Speed | Price | Best For |
|-------|---------|-----------|-----------------|-----------------|-------|-------|----------|
| **PC817** | DIP-4 | 5kV | 50mA | 1.2V | Standard | $ | General purpose (RECOMMENDED) |
| **4N35** | DIP-6 | 7.5kV | 60mA | 1.3V | Standard | $ | Higher isolation needed |
| **EL817** | DIP-4 | 5kV | 50mA | 1.2V | Standard | $ | PC817 alternative |
| **6N137** | DIP-8 | 5kV | 30mA | 1.5V | High-speed | $$ | Fast switching (not needed here) |

### PC817 (Recommended Choice)

**Why PC817 is ideal for boiler alarms:**
- ✅ **Common and cheap** (~$0.10-0.20 each)
- ✅ **5kV isolation** (more than enough for safety)
- ✅ **50mA max current** (handles our 11-23mA easily)
- ✅ **DIP-4 package** (easy breadboard mounting)
- ✅ **Wide availability** (Digikey, Mouser, Amazon, eBay)
- ✅ **Proven reliability** in industrial applications

**PC817 Specifications:**
```
Operating Temperature: -55°C to +100°C
Storage Temperature: -55°C to +125°C
LED Forward Current: 50mA maximum, 10mA typical
LED Forward Voltage: 1.2V typical @ 10mA
Isolation Voltage: 5000V AC (1 minute test)
Response Time: 4μs typical (plenty fast for alarms)
```

### Alternative: 4N35 (Higher Isolation)

Use 4N35 if you need extra safety margin:
- **7.5kV isolation** vs PC817's 5kV
- **DIP-6 package** (pins 3,6 not used for basic application)
- Same wiring as PC817, just different pin spacing

```
4N35 Pinout (DIP-6):
    ┌─────┐
  1 │●    │ 6  NC (not connected)
    │     │
  2 │     │ 5  Collector
    │     │
  3 │     │ 4  Emitter
    └─────┘

Pin 1: LED Anode
Pin 2: LED Cathode  
Pin 4: Transistor Emitter
Pin 5: Transistor Collector
```

## Wiring Connections

### Permanent Installation Options

**Option 1: Terminal Block Connection (Recommended)**
```
Boiler Alarm → Terminal Block → PC817 → Terminal Block → Raspberry Pi

Advantages:
- Easy maintenance and troubleshooting
- No soldering required
- Can disconnect/reconnect easily
- Professional appearance
```

**Option 2: Direct Wire with Wire Nuts**
```
Boiler Alarm → Wire Nuts → PC817 → Wire Nuts → Raspberry Pi GPIO

Advantages:
- Most compact
- Very reliable connections
- Standard electrical practice
```

**Option 3: Small PCB/Perfboard (Best for Multiple Sensors)**
```
Mount PC817 and resistors on small perfboard
Use screw terminals for external connections

Advantages:
- Most professional
- Good for multiple alarm inputs
- Easy to mount in enclosure
```

### Basic Alarm Input (Isolated) - 12-24V DC

**Terminal Block Method (Recommended for Permanent Install):**
```
Boiler Alarm Output (12-24V DC) → Terminal Block → PC817 → Terminal Block → Raspberry Pi GPIO

Terminal Block 1 (Alarm Side):
[Alarm +] → [1kΩ Resistor] → [PC817 Pin 1]
[Alarm -] → [PC817 Pin 2]

Terminal Block 2 (Pi Side):  
[3.3V] → [10kΩ Resistor] → [GPIO 18]
[3.3V] → [PC817 Pin 4]
[GPIO 18] → [PC817 Pin 3] 
[Ground] → [Pi Ground]
```

**Wire Nut Method:**
```
1. Strip 1/2" of insulation from all wires
2. Twist connections with wire nuts:
   - Alarm (+) + 1kΩ resistor lead + PC817 Pin 1 wire
   - Alarm (-) + PC817 Pin 2 wire  
   - 3.3V + 10kΩ resistor + PC817 Pin 4 wire
   - GPIO 18 + PC817 Pin 3 wire + 10kΩ resistor
   - Pi Ground + ground wire
3. Insulate with electrical tape
```

**PC817 Pinout (DIP-4 package):**
```
    ┌─────┐
  1 │●    │ 4  (● = Pin 1 indicator)
    │     │
  2 │     │ 3
    └─────┘

Pin 1: LED Anode    (connect to +12V/24V via 1kΩ resistor)
Pin 2: LED Cathode  (connect to alarm ground)
Pin 3: Transistor Emitter (connect to GPIO pin)
Pin 4: Transistor Collector (connect to 3.3V)
```

**Current Calculations:**
- For 12V: (12V - 1.2V) / 1kΩ = ~11mA (well within 50mA limit)
- For 24V: (24V - 1.2V) / 1kΩ = ~23mA (well within 50mA limit)

### Direct Connection (NOT RECOMMENDED for 12-24V systems)

```
⚠️ DANGER: DO NOT USE FOR 12-24V SYSTEMS ⚠️
This connection is ONLY for 3.3V logic level systems
```

**⚠️ CRITICAL WARNING**: Never connect 12-24V directly to Raspberry Pi GPIO pins!
- Raspberry Pi GPIO pins are 3.3V maximum
- 12-24V input will permanently damage the GPIO pins
- Always use optocoupler isolation for higher voltage systems
- Direct connection should only be used for 3.3V logic level alarm outputs

### Status LEDs (Optional)

```
Green LED (System OK):
GPIO 16 (Pin 36) → 220Ω Resistor → LED Anode
LED Cathode → Ground (Pin 34)

Red LED (Alarm Active):
GPIO 20 (Pin 38) → 220Ω Resistor → LED Anode
LED Cathode → Ground (Pin 39)

Blue LED (Network Status):
GPIO 21 (Pin 40) → 220Ω Resistor → LED Anode
LED Cathode → Ground (Pin 39)
```

### Local Buzzer (Optional)

```
5V Buzzer:
5V (Pin 2) → Buzzer (+)
GPIO 26 (Pin 37) → Buzzer (-)

3.3V Buzzer:
GPIO 26 (Pin 37) → Buzzer (+)
Ground (Pin 37) → Buzzer (-)
```

## Raspberry Pi GPIO Pinout Reference

```
     3.3V  (1) (2)  5V
    GPIO2  (3) (4)  5V
    GPIO3  (5) (6)  GND
    GPIO4  (7) (8)  GPIO14
      GND  (9) (10) GPIO15
   GPIO17 (11) (12) GPIO18  ← ALARM INPUT
   GPIO27 (13) (14) GND
   GPIO22 (15) (16) GPIO23
     3.3V (17) (18) GPIO24
   GPIO10 (19) (20) GND
    GPIO9 (21) (22) GPIO25
   GPIO11 (23) (24) GPIO8
      GND (25) (26) GPIO7
    GPIO0 (27) (28) GPIO1
    GPIO5 (29) (30) GND
    GPIO6 (31) (32) GPIO12
   GPIO13 (33) (34) GND
   GPIO19 (35) (36) GPIO16  ← GREEN LED
   GPIO26 (37) (38) GPIO20  ← RED LED
      GND (39) (40) GPIO21  ← BLUE LED
```

## Safety Considerations

### Electrical Isolation
- Always use optocouplers when connecting to external alarm systems
- Never connect higher voltage systems directly to GPIO pins
- Ensure proper grounding and avoid ground loops

### Power Requirements
- Raspberry Pi requires stable 5V power supply
- Consider UPS backup power for critical installations
- Monitor power consumption if adding many peripherals

### Environmental Protection
- Use appropriate enclosure for installation environment
- Consider temperature, humidity, and vibration
- Ensure adequate ventilation for Raspberry Pi

## Testing Connections

### Continuity Testing
1. Power off all systems before making connections
2. Use multimeter to verify connections
3. Check for short circuits before applying power

### GPIO Testing
```bash
# Test GPIO pin states
gpio readall

# Test specific pin (requires wiringpi)
gpio read 18
```

### Software Testing
```bash
# Run system in simulation mode first
SIMULATION_MODE=True python3 main.py

# Send test alert
python3 -c "from services.email_service import EmailService; from config.settings import Settings; EmailService(Settings()).send_test_alert()"
```

## Troubleshooting

### Common Issues
1. **No alarm detection**: Check wiring, pull-up resistors, active state configuration
2. **False alarms**: Adjust debounce time, check for electrical noise
3. **Email failures**: Verify SMTP settings, network connectivity
4. **GPIO errors**: Check permissions, ensure GPIO not in use by other processes

### Debug Commands
```bash
# Check GPIO status
sudo cat /sys/kernel/debug/gpio

# Monitor GPIO pin in real-time
watch -n 0.1 'gpio read 18'

# Check system logs
sudo journalctl -f -u boiler-alarm

# Test email connectivity
python3 -c "from services.email_service import EmailService; from config.settings import Settings; print(EmailService(Settings()).validate_connection())"

# Test alarm voltage (use multimeter):
# Measure between alarm (+) and (-) terminals
# Should read 12-24V DC when alarm is active
# Should read 0V or very low when alarm is inactive

# Test PC817 LED side (alarm must be active):
# Multimeter across pins 1-2 should read ~1.2V
# If no voltage, check alarm system and 1kΩ resistor

# Test PC817 transistor side:
# GPIO pin should read LOW (0V) when alarm is active
# GPIO pin should read HIGH (3.3V) when alarm is inactive
```