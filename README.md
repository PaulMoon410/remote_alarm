# Boiler Alarm Monitoring System

A Raspberry Pi-based monitoring system that detects boiler alarm signals and automatically sends email alerts to building superintendents and maintenance staff.

## 🚨 Features

- **Real-time Monitoring**: Continuously monitors GPIO pins for boiler alarm signals
- **Email Alerts**: Sends immediate email notifications when alarms are detected
- **SMS Support**: Email-to-SMS gateway support for mobile notifications
- **Debouncing**: Prevents false alarms with configurable debounce timing
- **Cooldown Period**: Prevents spam alerts with configurable cooldown periods
- **Systemd Integration**: Runs as a system service with automatic startup
- **Simulation Mode**: Test functionality without hardware
- **Comprehensive Logging**: Detailed logs for troubleshooting
- **Easy Configuration**: Environment variable-based configuration

## 🏗️ Hardware Requirements

### Raspberry Pi
- **Raspberry Pi 3 Model B/B+** (perfect for this application)
- Raspberry Pi 4 Model B (if you already have one)
- Raspberry Pi Zero W/2W (for minimal installations)
- MicroSD card (16GB minimum, Class 10)
- 5V power supply (2A for Pi 3, 2.5A for Pi 4)

### Electrical Components
- Optocoupler (PC817 or similar) for electrical isolation
- 10kΩ pull-up resistors
- Breadboard and jumper wires
- Optional: Status LEDs and buzzers

## 📦 Installation

### 1. Prepare the Raspberry Pi

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Clone the project
git clone <repository-url> /home/pi/boiler-alarm
cd /home/pi/boiler-alarm

# Run setup script
python3 setup.py
```

### 2. Configure Email Settings

```bash
# Copy environment template
cp config/.env.example .env

# Edit configuration
nano .env
```

Update the `.env` file with your email settings:

```bash
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=True

# Alert Recipients (comma-separated)
ALERT_RECIPIENTS=super@building.com,5551234567@vtext.com

# Building Information
BUILDING_NAME=Main Building
BUILDING_ADDRESS=123 Main St, City, State 12345
SUPER_NAME=John Smith

# GPIO Configuration
ALARM_GPIO_PIN=18
ALARM_ACTIVE_STATE=LOW
```

### 3. Test the System

```bash
# Test email configuration
python3 utils.py test-email

# Test GPIO (on Raspberry Pi)
python3 utils.py test-gpio

# Check system status
python3 utils.py status

# Trigger test alarm
python3 utils.py test-alarm
```

### 4. Install as System Service

```bash
# Install the service
sudo systemd/install_service.sh

# Start the service
sudo systemctl start boiler-alarm

# Enable automatic startup
sudo systemctl enable boiler-alarm

# Check service status
sudo systemctl status boiler-alarm

# View logs
sudo journalctl -f -u boiler-alarm
```

## 🔌 Hardware Wiring

### Basic Alarm Input (Recommended - Isolated)

```
Boiler Alarm System → Optocoupler → Raspberry Pi

Alarm Output (+) → PC817 Pin 1 (LED Anode)
Alarm Output (-) → PC817 Pin 2 (LED Cathode)

3.3V → 10kΩ Resistor → GPIO 18 (Pin 12)
3.3V → PC817 Pin 4 (Collector)
GPIO 18 → PC817 Pin 3 (Emitter)
Ground → Pi Ground (Pin 6)
```

### GPIO Pin Assignment

| Function | GPIO Pin | Physical Pin | Notes |
|----------|----------|--------------|-------|
| Alarm Input | GPIO 18 | Pin 12 | Main alarm signal |
| Status LED (Green) | GPIO 16 | Pin 36 | System OK |
| Status LED (Red) | GPIO 20 | Pin 38 | Alarm Active |
| Status LED (Blue) | GPIO 21 | Pin 40 | Network Status |
| Local Buzzer | GPIO 26 | Pin 37 | Optional local alarm |

See [hardware/wiring_guide.md](hardware/wiring_guide.md) for detailed wiring instructions.

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ALARM_GPIO_PIN` | 18 | GPIO pin for alarm input |
| `GPIO_PULL_UP` | True | Enable internal pull-up resistor |
| `ALARM_ACTIVE_STATE` | LOW | Active state (LOW or HIGH) |
| `SMTP_SERVER` | smtp.gmail.com | SMTP server address |
| `SMTP_PORT` | 587 | SMTP server port |
| `SMTP_USERNAME` | | Your email username |
| `SMTP_PASSWORD` | | Your email password/app password |
| `ALERT_RECIPIENTS` | | Comma-separated email addresses |
| `BUILDING_NAME` | Main Building | Building name for alerts |
| `CHECK_INTERVAL` | 0.1 | GPIO check interval (seconds) |
| `DEBOUNCE_TIME` | 2.0 | Alarm debounce time (seconds) |
| `ALERT_COOLDOWN` | 300 | Alert cooldown period (seconds) |
| `SIMULATION_MODE` | False | Enable simulation mode |

### Email-to-SMS Gateway

For SMS alerts, use carrier email-to-SMS gateways:

| Carrier | Gateway Format |
|---------|----------------|
| Verizon | `5551234567@vtext.com` |
| AT&T | `5551234567@txt.att.net` |
| T-Mobile | `5551234567@tmomail.net` |
| Sprint | `5551234567@messaging.sprintpcs.com` |

## 🧪 Testing

### Unit Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test
python3 tests/test_boiler_alarm.py
```

### Manual Testing

```bash
# Test email functionality
python3 utils.py test-email

# Test GPIO pins
python3 utils.py test-gpio

# Trigger test alarm
python3 utils.py test-alarm

# Monitor system status
python3 utils.py status
```

### Simulation Mode

For development and testing without hardware:

```bash
export SIMULATION_MODE=True
python3 main.py
```

## 📊 Monitoring and Logs

### View Live Logs

```bash
# Service logs
sudo journalctl -f -u boiler-alarm

# Application logs
tail -f logs/boiler_alarm.log
```

### System Status

```bash
# Service status
sudo systemctl status boiler-alarm

# GPIO status
gpio readall

# System status
python3 utils.py status
```

## 🔧 Troubleshooting

### Common Issues

#### Email Not Sending
- Check SMTP credentials
- Verify network connectivity
- Enable "Less secure app access" or use app passwords
- Check firewall settings

```bash
python3 utils.py test-email
```

#### GPIO Not Working
- Check wiring connections
- Verify GPIO pin assignment
- Test pin states manually

```bash
python3 utils.py test-gpio
gpio read 18
```

#### False Alarms
- Increase debounce time
- Check for electrical noise
- Verify alarm active state configuration

#### Service Not Starting
- Check service logs: `sudo journalctl -u boiler-alarm`
- Verify file permissions
- Check Python dependencies

### Debug Commands

```bash
# Check GPIO status
sudo cat /sys/kernel/debug/gpio

# Monitor GPIO pin
watch -n 0.1 'gpio read 18'

# Test email connectivity
python3 -c "from services.email_service import EmailService; from config.settings import Settings; print(EmailService(Settings()).validate_connection())"

# Check service status
sudo systemctl status boiler-alarm
```

## 📁 Project Structure

```
boiler-alarm/
├── main.py                 # Main application entry point
├── utils.py                # Utility scripts and CLI tools
├── setup.py                # Installation script
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration (create from .env.example)
│
├── config/
│   ├── settings.py         # Configuration management
│   └── .env.example        # Environment template
│
├── services/
│   ├── alarm_monitor.py    # GPIO monitoring logic
│   └── email_service.py    # Email alert functionality
│
├── hardware/
│   ├── gpio_pins.py        # GPIO pin definitions
│   └── wiring_guide.md     # Detailed wiring instructions
│
├── systemd/
│   ├── boiler-alarm.service # Systemd service file
│   └── install_service.sh   # Service installation script
│
├── tests/
│   └── test_boiler_alarm.py # Unit tests
│
└── logs/
    └── boiler_alarm.log     # Application logs
```

## 🔒 Security Considerations

- **Electrical Isolation**: Always use optocouplers for external connections
- **Network Security**: Use strong passwords and secure network connections
- **Email Security**: Use app passwords instead of account passwords
- **File Permissions**: Restrict access to configuration files containing credentials

## 📞 Support

For issues, questions, or contributions:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Test individual components using the utility scripts
4. Submit issues with detailed error logs and hardware configuration

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for building maintenance and safety applications
- Designed for 24/7 reliable operation
- Tested on Raspberry Pi 3B+ and 4B platforms