"""
Alarm monitoring service for detecting boiler alarm signals.
Handles GPIO pin monitoring with debouncing and alert management.
"""

import time
import logging
import threading
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import RPi.GPIO, fall back to simulation if not available
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    logger.warning("RPi.GPIO not available, running in simulation mode")

class AlarmMonitor:
    """Monitors GPIO pins for boiler alarm signals."""
    
    def __init__(self, settings, email_service):
        self.settings = settings
        self.email_service = email_service
        self.monitoring = False
        self.last_alert_time: Optional[datetime] = None
        self.alarm_start_time: Optional[datetime] = None
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Initialize GPIO if available and not in simulation mode
        self.gpio_initialized = False
        if GPIO_AVAILABLE and not self.settings.simulation_mode:
            self._init_gpio()
    
    def _init_gpio(self):
        """Initialize GPIO pin for alarm monitoring."""
        try:
            GPIO.setmode(GPIO.BCM)
            
            # Set up the alarm pin
            if self.settings.gpio_pull_up:
                GPIO.setup(
                    self.settings.alarm_gpio_pin, 
                    GPIO.IN, 
                    pull_up_down=GPIO.PUD_UP
                )
            else:
                GPIO.setup(
                    self.settings.alarm_gpio_pin, 
                    GPIO.IN, 
                    pull_up_down=GPIO.PUD_DOWN
                )
            
            self.gpio_initialized = True
            logger.info(f"GPIO pin {self.settings.alarm_gpio_pin} initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize GPIO: {e}")
            self.gpio_initialized = False
    
    def start_monitoring(self):
        """Start monitoring the alarm pin."""
        if self.monitoring:
            logger.warning("Monitoring is already running")
            return
        
        self.monitoring = True
        
        if self.settings.simulation_mode:
            logger.info("Starting alarm monitoring in SIMULATION MODE")
            self.monitor_thread = threading.Thread(target=self._simulation_monitor_loop)
        else:
            logger.info("Starting alarm monitoring on GPIO pin")
            self.monitor_thread = threading.Thread(target=self._gpio_monitor_loop)
        
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring the alarm pin."""
        self.monitoring = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        if self.gpio_initialized:
            GPIO.cleanup()
            logger.info("GPIO cleanup completed")
    
    def _gpio_monitor_loop(self):
        """Main monitoring loop for GPIO pin."""
        if not self.gpio_initialized:
            logger.error("GPIO not initialized, cannot start monitoring")
            return
        
        alarm_active = False
        
        while self.monitoring:
            try:
                # Read GPIO pin state
                pin_state = GPIO.input(self.settings.alarm_gpio_pin)
                
                # Determine if alarm is active based on configuration
                is_alarm_triggered = (
                    (self.settings.alarm_active_state == 'LOW' and pin_state == GPIO.LOW) or
                    (self.settings.alarm_active_state == 'HIGH' and pin_state == GPIO.HIGH)
                )
                
                if is_alarm_triggered and not alarm_active:
                    # Alarm just triggered
                    self.alarm_start_time = datetime.now()
                    logger.warning("Alarm signal detected, starting debounce period")
                    alarm_active = True
                    
                elif is_alarm_triggered and alarm_active:
                    # Alarm is still active, check if debounce time has passed
                    if self.alarm_start_time:
                        elapsed = (datetime.now() - self.alarm_start_time).total_seconds()
                        if elapsed >= self.settings.debounce_time:
                            self._handle_alarm_event()
                            
                elif not is_alarm_triggered and alarm_active:
                    # Alarm signal stopped
                    logger.info("Alarm signal cleared")
                    alarm_active = False
                    self.alarm_start_time = None
                
                time.sleep(self.settings.check_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(1)
    
    def _simulation_monitor_loop(self):
        """Simulation monitoring loop for testing without hardware."""
        logger.info("Simulation mode: Press Ctrl+C to trigger test alarm")
        
        # Send a test alert when starting simulation
        try:
            self.email_service.send_test_alert()
        except Exception as e:
            logger.error(f"Failed to send test alert: {e}")
        
        while self.monitoring:
            time.sleep(1)
    
    def _handle_alarm_event(self):
        """Handle a confirmed alarm event."""
        current_time = datetime.now()
        
        # Check if we're still in cooldown period
        if self._is_in_cooldown(current_time):
            logger.info("Alarm detected but still in cooldown period")
            return
        
        logger.critical("🚨 BOILER ALARM CONFIRMED - SENDING ALERT 🚨")
        
        # Send alert
        try:
            success = self.email_service.send_alarm_alert(
                alarm_type="Boiler Alarm",
                additional_info=f"Alarm detected on GPIO pin {self.settings.alarm_gpio_pin}"
            )
            
            if success:
                self.last_alert_time = current_time
                logger.info("Alarm alert sent successfully")
            else:
                logger.error("Failed to send alarm alert")
                
        except Exception as e:
            logger.error(f"Error sending alarm alert: {e}")
    
    def _is_in_cooldown(self, current_time: datetime) -> bool:
        """Check if we're still in the alert cooldown period."""
        if not self.last_alert_time:
            return False
        
        cooldown_end = self.last_alert_time + timedelta(seconds=self.settings.alert_cooldown)
        return current_time < cooldown_end
    
    def trigger_test_alarm(self):
        """Manually trigger a test alarm (for testing purposes)."""
        logger.info("Triggering test alarm")
        self._handle_alarm_event()
    
    def get_status(self) -> dict:
        """Get current monitoring status."""
        status = {
            'monitoring': self.monitoring,
            'simulation_mode': self.settings.simulation_mode,
            'gpio_initialized': self.gpio_initialized,
            'gpio_pin': self.settings.alarm_gpio_pin,
            'last_alert_time': self.last_alert_time.isoformat() if self.last_alert_time else None,
            'in_cooldown': self._is_in_cooldown(datetime.now()) if self.last_alert_time else False
        }
        
        if not self.settings.simulation_mode and self.gpio_initialized:
            try:
                pin_state = GPIO.input(self.settings.alarm_gpio_pin)
                status['current_pin_state'] = 'HIGH' if pin_state == GPIO.HIGH else 'LOW'
            except:
                status['current_pin_state'] = 'ERROR'
        
        return status