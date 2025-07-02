import pyaudio
import wave
import os
import datetime
import threading
import time
import numpy as np
import struct

class AudioRecorder:
    def __init__(self, output_dir="audio_recordings", duration=3, sample_rate=44100):
        """Initialize audio recorder."""
        self.output_dir = output_dir
        self.duration = duration
        self.sample_rate = sample_rate
        self.channels = 2
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.running = False
        
        # Ensure directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def _record_audio(self):
        """Record audio for specified duration."""
        try:
            print(f"Recording audio for {self.duration} seconds...")
            
            p = pyaudio.PyAudio()
            
            # List all available audio devices for debugging
            print("\nAvailable audio devices:")
            info = p.get_host_api_info_by_index(0)
            num_devices = info.get('deviceCount')
            for i in range(num_devices):
                device_info = p.get_device_info_by_index(i)
                print(f"Device {i}: {device_info['name']} (in: {device_info['maxInputChannels']}, out: {device_info['maxOutputChannels']})")
            
            # Find the stereo mix device if available
            loopback_device_index = None
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                device_name = device_info["name"].lower()
                
                # Look for stereo mix or similar
                if "stereo mix" in device_name or "what u hear" in device_name:
                    loopback_device_index = i
                    print(f"Selected system audio device: {device_info['name']} (index: {i})")
                    break
            
            # If no stereo mix, fall back to default input device
            if loopback_device_index is None:
                loopback_device_index = p.get_default_input_device_info()["index"]
                print(f"No system audio device found. Using default input: {p.get_device_info_by_index(loopback_device_index)['name']}")
            
            # Open stream with selected device
            stream = p.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk,
                input_device_index=loopback_device_index
            )
            
            print(f"Started recording with {p.get_device_info_by_index(loopback_device_index)['name']}")
            print("Make sure audio is playing on your system while recording")
            
            frames = []
            has_audio = False
            
            # Calculate how many chunks to record
            num_chunks = int((self.sample_rate / self.chunk) * self.duration)
            
            for i in range(0, num_chunks):
                data = stream.read(self.chunk, exception_on_overflow=False)
                frames.append(data)
                
                # Check if there's actual audio (not silence)
                if i % 10 == 0:  # Check every 10th chunk
                    # Convert bytes to integers
                    fmt = "%dh" % (len(data) // 2)
                    data_int = struct.unpack(fmt, data)
                    
                    # Calculate RMS
                    rms = np.sqrt(np.mean(np.array(data_int)**2))
                    db = 20 * np.log10(rms) if rms > 0 else -100
                    
                    if db > -50:  # If volume above threshold
                        has_audio = True
                        print(f"Audio detected: {db:.1f}dB", end="\r")
            
            # Stop and close the stream
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            if not has_audio:
                print("\nWarning: No significant audio detected. The recording might be silent.")
                print("Make sure your system audio was playing during recording.")
            else:
                print("\nAudio detected in the recording.")
            
            # Generate filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"system_audio_{timestamp}.wav")
            
            # Save recording to a WAV file
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            print(f"Audio saved: {filename}")
            return filename
        except Exception as e:
            print(f"Error recording audio: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _recording_loop(self):
        """Main recording loop."""
        while self.running:
            self._record_audio()
            # Small delay between recordings
            time.sleep(1)
    
    def start(self):
        """Start audio recorder."""
        print(f"Starting audio recorder, saving to {self.output_dir}")
        self.running = True
        
        self.thread = threading.Thread(target=self._recording_loop)
        self.thread.daemon = True
        self.thread.start()
        return self
    
    def stop(self):
        """Stop audio recorder."""
        if self.running:
            self.running = False
            print("Audio recorder stopped")