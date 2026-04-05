"""
Unit tests for the boiler alarm monitoring system.
Tests email service, alarm detection, and configuration.
"""

import unittest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Import modules to test
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import Settings
from services.email_service import EmailService
from services.alarm_monitor import AlarmMonitor

class TestSettings(unittest.TestCase):
    """Test configuration settings."""
    
    def setUp(self):
        """Set up test environment variables."""
        # Set required environment variables for testing
        os.environ.update({
            'SMTP_USERNAME': 'test@example.com',
            'SMTP_PASSWORD': 'test_password',
            'ALERT_RECIPIENTS': 'admin@building.com,super@building.com',
            'SIMULATION_MODE': 'True'
        })
    
    def tearDown(self):
        """Clean up environment variables."""
        test_vars = [
            'SMTP_USERNAME', 'SMTP_PASSWORD', 'ALERT_RECIPIENTS',
            'SIMULATION_MODE', 'ALARM_GPIO_PIN', 'BUILDING_NAME'
        ]
        for var in test_vars:
            os.environ.pop(var, None)
    
    def test_default_settings(self):
        """Test default configuration values."""
        settings = Settings()
        
        self.assertEqual(settings.alarm_gpio_pin, 18)
        self.assertEqual(settings.smtp_server, 'smtp.gmail.com')
        self.assertEqual(settings.smtp_port, 587)
        self.assertTrue(settings.simulation_mode)
    
    def test_custom_settings(self):
        """Test custom configuration values."""
        os.environ.update({
            'ALARM_GPIO_PIN': '22',
            'BUILDING_NAME': 'Test Building',
            'CHECK_INTERVAL': '0.5'
        })
        
        settings = Settings()
        
        self.assertEqual(settings.alarm_gpio_pin, 22)
        self.assertEqual(settings.building_name, 'Test Building')
        self.assertEqual(settings.check_interval, 0.5)
    
    def test_validation_missing_username(self):
        """Test validation with missing SMTP username."""
        del os.environ['SMTP_USERNAME']
        
        with self.assertRaises(ValueError):
            Settings()
    
    def test_validation_missing_recipients(self):
        """Test validation with missing alert recipients."""
        del os.environ['ALERT_RECIPIENTS']
        
        with self.assertRaises(ValueError):
            Settings()

class TestEmailService(unittest.TestCase):
    """Test email service functionality."""
    
    def setUp(self):
        """Set up test email service."""
        os.environ.update({
            'SMTP_USERNAME': 'test@example.com',
            'SMTP_PASSWORD': 'test_password',
            'ALERT_RECIPIENTS': 'admin@building.com,super@building.com',
            'BUILDING_NAME': 'Test Building',
            'SIMULATION_MODE': 'True'
        })
        
        self.settings = Settings()
        self.email_service = EmailService(self.settings)
    
    def tearDown(self):
        """Clean up environment variables."""
        test_vars = [
            'SMTP_USERNAME', 'SMTP_PASSWORD', 'ALERT_RECIPIENTS',
            'BUILDING_NAME', 'SIMULATION_MODE'
        ]
        for var in test_vars:
            os.environ.pop(var, None)
    
    @patch('smtplib.SMTP')
    def test_send_alarm_alert(self, mock_smtp):
        """Test sending alarm alert."""
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Send alert
        result = self.email_service.send_alarm_alert()
        
        # Verify email was sent
        self.assertTrue(result)
        mock_server.login.assert_called_once()
        self.assertEqual(mock_server.sendmail.call_count, 2)  # Two recipients
    
    @patch('smtplib.SMTP')
    def test_send_test_alert(self, mock_smtp):
        """Test sending test alert."""
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Send test alert
        result = self.email_service.send_test_alert()
        
        # Verify test email was sent
        self.assertTrue(result)
        mock_server.login.assert_called_once()
    
    def test_create_alert_message(self):
        """Test alert message creation."""
        message = self.email_service._create_alert_message("Test Alarm", "Additional info")
        
        self.assertIn("🚨 BOILER ALARM ACTIVATED 🚨", message)
        self.assertIn("Test Building", message)
        self.assertIn("Test Alarm", message)
        self.assertIn("Additional info", message)
    
    @patch('smtplib.SMTP')
    def test_validate_connection(self, mock_smtp):
        """Test SMTP connection validation."""
        # Mock successful connection
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = self.email_service.validate_connection()
        
        self.assertTrue(result)
        mock_server.login.assert_called_once()

class TestAlarmMonitor(unittest.TestCase):
    """Test alarm monitoring functionality."""
    
    def setUp(self):
        """Set up test alarm monitor."""
        os.environ.update({
            'SMTP_USERNAME': 'test@example.com',
            'SMTP_PASSWORD': 'test_password',
            'ALERT_RECIPIENTS': 'admin@building.com',
            'SIMULATION_MODE': 'True',
            'DEBOUNCE_TIME': '1.0',
            'ALERT_COOLDOWN': '60'
        })
        
        self.settings = Settings()
        self.email_service = Mock()
        self.alarm_monitor = AlarmMonitor(self.settings, self.email_service)
    
    def tearDown(self):
        """Clean up test environment."""
        if self.alarm_monitor.monitoring:
            self.alarm_monitor.stop_monitoring()
        
        test_vars = [
            'SMTP_USERNAME', 'SMTP_PASSWORD', 'ALERT_RECIPIENTS',
            'SIMULATION_MODE', 'DEBOUNCE_TIME', 'ALERT_COOLDOWN'
        ]
        for var in test_vars:
            os.environ.pop(var, None)
    
    def test_initialization(self):
        """Test alarm monitor initialization."""
        self.assertEqual(self.alarm_monitor.settings, self.settings)
        self.assertEqual(self.alarm_monitor.email_service, self.email_service)
        self.assertFalse(self.alarm_monitor.monitoring)
    
    def test_handle_alarm_event(self):
        """Test alarm event handling."""
        # Trigger alarm event
        self.alarm_monitor._handle_alarm_event()
        
        # Verify email service was called
        self.email_service.send_alarm_alert.assert_called_once()
    
    def test_cooldown_period(self):
        """Test alert cooldown functionality."""
        # Set last alert time to now
        self.alarm_monitor.last_alert_time = datetime.now()
        
        # Check that we're in cooldown
        current_time = datetime.now()
        self.assertTrue(self.alarm_monitor._is_in_cooldown(current_time))
        
        # Check that cooldown expires
        future_time = datetime.now() + timedelta(seconds=70)
        self.assertFalse(self.alarm_monitor._is_in_cooldown(future_time))
    
    def test_get_status(self):
        """Test status reporting."""
        status = self.alarm_monitor.get_status()
        
        self.assertIn('monitoring', status)
        self.assertIn('simulation_mode', status)
        self.assertIn('gpio_pin', status)
        self.assertEqual(status['simulation_mode'], True)
        self.assertEqual(status['gpio_pin'], 18)
    
    def test_trigger_test_alarm(self):
        """Test manual alarm triggering."""
        self.alarm_monitor.trigger_test_alarm()
        
        # Verify email service was called
        self.email_service.send_alarm_alert.assert_called_once()

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        """Set up integration test environment."""
        os.environ.update({
            'SMTP_USERNAME': 'test@example.com',
            'SMTP_PASSWORD': 'test_password',
            'ALERT_RECIPIENTS': 'admin@building.com',
            'SIMULATION_MODE': 'True',
            'BUILDING_NAME': 'Integration Test Building'
        })
    
    def tearDown(self):
        """Clean up integration test environment."""
        test_vars = [
            'SMTP_USERNAME', 'SMTP_PASSWORD', 'ALERT_RECIPIENTS',
            'SIMULATION_MODE', 'BUILDING_NAME'
        ]
        for var in test_vars:
            os.environ.pop(var, None)
    
    @patch('smtplib.SMTP')
    def test_full_system_workflow(self, mock_smtp):
        """Test complete system workflow."""
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Initialize system components
        settings = Settings()
        email_service = EmailService(settings)
        alarm_monitor = AlarmMonitor(settings, email_service)
        
        # Test system status
        status = alarm_monitor.get_status()
        self.assertFalse(status['monitoring'])
        
        # Test email validation
        self.assertTrue(email_service.validate_connection())
        
        # Test alarm trigger
        alarm_monitor.trigger_test_alarm()
        
        # Verify email was sent
        mock_server.login.assert_called()

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    logs_dir = project_root / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Run tests
    unittest.main(verbosity=2)