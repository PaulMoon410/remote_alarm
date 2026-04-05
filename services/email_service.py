"""
Email service for sending boiler alarm notifications.
Supports both regular email and email-to-SMS alerts.
"""

import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending email alerts about boiler alarms."""
    
    def __init__(self, settings):
        self.settings = settings
        
    def send_alarm_alert(self, alarm_type: str = "Boiler Alarm", additional_info: str = ""):
        """Send an alarm alert to all configured recipients."""
        try:
            subject = f"🚨 {alarm_type} - {self.settings.building_name}"
            body = self._create_alert_message(alarm_type, additional_info)
            
            self._send_email(
                subject=subject,
                body=body,
                recipients=self.settings.alert_recipients
            )
            
            logger.info(f"Alarm alert sent to {len(self.settings.alert_recipients)} recipients")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send alarm alert: {e}")
            return False
    
    def send_test_alert(self):
        """Send a test alert to verify the system is working."""
        try:
            subject = f"✅ Test Alert - {self.settings.building_name}"
            body = self._create_test_message()
            
            self._send_email(
                subject=subject,
                body=body,
                recipients=self.settings.alert_recipients
            )
            
            logger.info("Test alert sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send test alert: {e}")
            return False
    
    def _create_alert_message(self, alarm_type: str, additional_info: str) -> str:
        """Create the body of an alarm alert message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
🚨 BOILER ALARM ACTIVATED 🚨

Building: {self.settings.building_name}
Address: {self.settings.building_address}
Alarm Type: {alarm_type}
Time: {timestamp}

IMMEDIATE ACTION REQUIRED

This is an automated alert from the boiler monitoring system. 
A boiler alarm has been detected and requires immediate attention.

Contact: {self.settings.super_name}

{additional_info}

---
Boiler Alarm Monitoring System
        """.strip()
        
        return message
    
    def _create_test_message(self) -> str:
        """Create the body of a test message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
✅ Boiler Alarm System Test

Building: {self.settings.building_name}
Address: {self.settings.building_address}
Test Time: {timestamp}

This is a test message from the boiler alarm monitoring system.
The system is operational and able to send alerts.

If you receive this message, the alert system is working correctly.

Contact: {self.settings.super_name}

---
Boiler Alarm Monitoring System
        """.strip()
        
        return message
    
    def _send_email(self, subject: str, body: str, recipients: List[str]):
        """Send an email using SMTP."""
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.settings.alert_sender
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to server and send email
        with smtplib.SMTP(self.settings.smtp_server, self.settings.smtp_port) as server:
            if self.settings.use_tls:
                server.starttls()
            
            server.login(self.settings.smtp_username, self.settings.smtp_password)
            
            for recipient in recipients:
                msg['To'] = recipient
                text = msg.as_string()
                server.sendmail(self.settings.alert_sender, recipient, text)
                
                # Remove the 'To' header for the next recipient
                del msg['To']
        
        logger.info(f"Email sent to: {', '.join(recipients)}")
    
    def validate_connection(self) -> bool:
        """Test the SMTP connection without sending an email."""
        try:
            with smtplib.SMTP(self.settings.smtp_server, self.settings.smtp_port) as server:
                if self.settings.use_tls:
                    server.starttls()
                server.login(self.settings.smtp_username, self.settings.smtp_password)
            
            logger.info("SMTP connection validated successfully")
            return True
            
        except Exception as e:
            logger.error(f"SMTP connection failed: {e}")
            return False