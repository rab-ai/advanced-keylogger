import win32clipboard
import time
import os
import datetime
import threading

class ClipboardMonitor:
    def __init__(self, output_file="clipboard_data.txt", polling_interval=3):
        """Initialize the clipboard monitor."""
        self.output_file = output_file
        self.polling_interval = polling_interval
        self.previous_content = ""
        self.running = False
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    def _get_clipboard_content(self):
        """Get current clipboard content."""
        try:
            win32clipboard.OpenClipboard()
            try:
                data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            except:
                data = None
            finally:
                win32clipboard.CloseClipboard()
            return data
        except Exception as e:
            print(f"Error accessing clipboard: {e}")
            return None
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.running:
            try:
                content = self._get_clipboard_content()
                
                # If content is valid and different from previous
                if content and content != self.previous_content:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    with open(self.output_file, 'a', encoding='utf-8') as f:
                        f.write(f"\n[{timestamp}] Clipboard Content:\n")
                        f.write("-" * 40 + "\n")
                        f.write(content)
                        f.write("\n" + "-" * 40 + "\n")
                    
                    # Update previous content
                    self.previous_content = content
            except Exception as e:
                print(f"Error in clipboard monitoring: {e}")
            
            time.sleep(self.polling_interval)
    
    def start(self):
        """Start monitoring clipboard."""
        print(f"Starting clipboard monitor, output will be saved to {self.output_file}")
        self.running = True
        
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.daemon = True
        self.thread.start()
        return self
    
    def stop(self):
        """Stop monitoring clipboard."""
        if self.running:
            self.running = False
            print("Clipboard monitor stopped")