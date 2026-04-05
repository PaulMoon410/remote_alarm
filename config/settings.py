"""
Configuration settings for the boiler alarm monitoring system.
Loads settings from environment variables and configuration files.
"""

import os
from typing import List
from pathlib import Path

class Settings:
    """Configuration settings for the boiler alarm system."""
    
    def __init__(self):
        # Load environment variables with defaults
        self.load_settings()
    
    def load_settings(self):
        """Load all configuration settings."""
        # GPIO Configuration
        self.alarm_gpio_pin = int(os.getenv('ALARM_GPIO_PIN', '18'))  # Default GPIO 18
        self.gpio_pull_up = os.getenv('GPIO_PULL_UP', 'True').lower() == 'true'
        self.alarm_active_state = os.getenv('ALARM_ACTIVE_STATE', 'LOW').upper()  # LOW or HIGH
        
        # Email Configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.use_tls = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
        
        # Alert Configuration
        self.alert_sender = os.getenv('ALERT_SENDER', self.smtp_username)
        recipients_str = os.getenv('ALERT_RECIPIENTS', '')
        self.alert_recipients = [email.strip() for email in recipients_str.split(',') if email.strip()]
        
        # Building information
        self.building_name = os.getenv('BUILDING_NAME', 'Main Building')
        self.building_address = os.getenv('BUILDING_ADDRESS', '')
        self.super_name = os.getenv('SUPER_NAME', 'Building Superintendent')
        
        # Monitoring Configuration
        self.check_interval = float(os.getenv('CHECK_INTERVAL', '0.1'))  # seconds
        self.debounce_time = float(os.getenv('DEBOUNCE_TIME', '2.0'))  # seconds
        self.alert_cooldown = int(os.getenv('ALERT_COOLDOWN', '300'))  # seconds (5 minutes)
        
        # System Configuration
        self.simulation_mode = os.getenv('SIMULATION_MODE', 'False').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate that required settings are present."""
        if not self.smtp_username:
            raise ValueError("SMTP_USERNAME environment variable is required")
        
        if not self.smtp_password:
            raise ValueError("SMTP_PASSWORD environment variable is required")
        
        if not self.alert_recipients:
            raise ValueError("ALERT_RECIPIENTS environment variable is required")
        
        if self.alarm_gpio_pin < 0 or self.alarm_gpio_pin > 27:
            raise ValueError("ALARM_GPIO_PIN must be between 0 and 27")
    
    def get_email_to_sms_addresses(self) -> List[str]:
        """
        Convert phone numbers to email-to-SMS addresses for major carriers.
        Assumes alert_recipients contains phone numbers that need conversion.
        """
        sms_gateways = {
            # Major US carriers
            'verizon': '@vtext.com',
            'att': '@txt.att.net', 
            'tmobile': '@tmomail.net',
            'sprint': '@messaging.sprintpcs.com',
            'cricket': '@sms.cricketwireless.net',
            'boost': '@smsmyboostmobile.com',
            'metro': '@mymetropcs.com'
        }
        
        # For now, return the recipients as-is
        # In production, you might want to detect phone numbers and convert them
        return self.alert_recipients
    
    def __str__(self):
        """String representation of settings (without sensitive data)."""
        return f"""Boiler Alarm Settings:
  GPIO Pin: {self.alarm_gpio_pin}
  Active State: {self.alarm_active_state}
  SMTP Server: {self.smtp_server}:{self.smtp_port}
  Building: {self.building_name}
  Recipients: {len(self.alert_recipients)} configured
  Simulation Mode: {self.simulation_mode}
"""