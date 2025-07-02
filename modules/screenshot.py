from PIL import ImageGrab
import os
import time
import datetime
import threading

class ScreenshotRecorder:
    def __init__(self, output_dir="screenshots", interval=10):
        """Initialize the screenshot recorder."""
        self.output_dir = output_dir
        self.interval = interval
        self.running = False
        
        # Ensure directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def _take_screenshot(self):
        """Capture and save a screenshot."""
        try:
            # Capture screenshot
            screenshot = ImageGrab.grab()
            
            # Generate filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"screenshot_{timestamp}.png")
            
            # Save the image
            screenshot.save(filename)
            print(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    def _screenshot_loop(self):
        """Main screenshot capture loop."""
        while self.running:
            self._take_screenshot()
            time.sleep(self.interval)
    
    def start(self):
        """Start capturing screenshots."""
        print(f"Starting screenshot recorder, saving to {self.output_dir}")
        self.running = True
        
        self.thread = threading.Thread(target=self._screenshot_loop)
        self.thread.daemon = True
        self.thread.start()
        return self
    
    def stop(self):
        """Stop capturing screenshots."""
        if self.running:
            self.running = False
            print("Screenshot recorder stopped")