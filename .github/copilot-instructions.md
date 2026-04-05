<!-- Boiler Alarm Monitoring System Instructions -->

This project is a Raspberry Pi-based boiler alarm monitoring system that:
- Monitors GPIO pins for boiler alarm signals
- Sends email alerts to building superintendents
- Uses email-to-SMS for mobile notifications
- Includes logging and systemd service setup
- Provides hardware wiring documentation

## Project Structure
- `main.py` - Main monitoring script
- `config/` - Configuration files for email, GPIO settings
- `services/` - Email service and alarm detection logic
- `hardware/` - GPIO pin definitions and hardware setup docs
- `logs/` - Log files and logging configuration
- `systemd/` - Service files for automatic startup
- `tests/` - Unit tests for the monitoring system

## Development Guidelines
- Use Python 3.7+ for Raspberry Pi compatibility
- Include proper error handling and logging
- Make email credentials configurable via environment variables
- Support both GPIO hardware and simulation mode for testing
- Follow Raspberry Pi GPIO best practices