#!/usr/bin/env python3
"""
Boiler Alarm Monitoring System
Main entry point for the boiler alarm monitoring service.
Monitors GPIO pins for alarm signals and sends email alerts.
"""

import os
import sys
import time
import signal
import logging
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import Settings
from services.alarm_monitor import AlarmMonitor
from services.email_service import EmailService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/boiler_alarm.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BoilerAlarmSystem:
    """Main system controller for boiler alarm monitoring."""
    
    def __init__(self):
        self.settings = Settings()
        self.email_service = EmailService(self.settings)
        self.alarm_monitor = AlarmMonitor(self.settings, self.email_service)
        self.running = False
        
    def start(self):
        """Start the monitoring system."""
        logger.info("Starting Boiler Alarm Monitoring System")
        logger.info(f"Monitoring GPIO pin: {self.settings.alarm_gpio_pin}")
        logger.info(f"Alert recipients: {', '.join(self.settings.alert_recipients)}")
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            self.running = True
            self.alarm_monitor.start_monitoring()
            
            # Main loop
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"System error: {e}")
            raise
        finally:
            self.stop()
    
    def stop(self):
        """Stop the monitoring system."""
        logger.info("Stopping Boiler Alarm Monitoring System")
        self.running = False
        if hasattr(self.alarm_monitor, 'stop_monitoring'):
            self.alarm_monitor.stop_monitoring()
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

def main():
    """Main entry point."""
    try:
        system = BoilerAlarmSystem()
        system.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()