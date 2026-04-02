import numpy as np
import customtkinter as ctk
import datetime, time, mss, cv2, threading

class ScreenRecorderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Recorder")
        self.geometry("300x250")
        
        self.recording = False
        self.setup_ui()

    def setup_ui(self):   
        # UI Elements
        self.label = ctk.CTkLabel(self, text="Screen Recorder", font=("Arial", 20))
        self.label.pack(pady=20)
        
        self.start_button = ctk.CTkButton(self, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)
        
        self.stop_button = ctk.CTkButton(self, text="Stop Recording", command=self.stop_recording, state="disabled")
        self.stop_button.pack(pady=10)

        self.take_screenshot = ctk.CTkButton(self, text="Screenshot", command=self.take_screenshot)
        self.take_screenshot.pack(pady=10)


    def start_recording(self):
        self.recording = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        # Run recording in a separate thread
        threading.Thread(target=self.record_loop, daemon=True).start()

    def stop_recording(self):
        self.recording = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def flash_animation(self):
        # Create a white fullscreen window
        flash = ctk.CTkToplevel(self)
        flash.overrideredirect(True)
        flash.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        flash.attributes("-topmost", True)
        flash.config(bg="white")
        
        # Quick fade effect
        for alpha in [0.8, 0.6, 0.4, 0.2, 0.0]:
            flash.attributes("-alpha", alpha)
            flash.update()
            time.sleep(0.05)
        flash.destroy()

    def take_screenshot(self):
        with mss.mss() as sct:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.iconify()
            time.sleep(0.4)
            sct.shot(mon=1, output=f'Screenshot_{timestamp}.png')
            self.flash_animation()

    def record_loop(self):
        # Initialize mss
        with mss.mss() as sct:
            self.iconify()
            time.sleep(0.3)
            monitor = sct.monitors[1]
            resolution = (monitor["width"], monitor["height"])
            
            codec = cv2.VideoWriter_fourcc(*"acv1")
            fps = 30.0 
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output = cv2.VideoWriter(f'Recording_{timestamp}.mp4', codec, fps, resolution)

            while self.recording:
                # Grab the screen data
                sct_img = sct.grab(monitor)
                
                # Convert the raw bytes to a numpy array
                frame = np.array(sct_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                
                output.write(frame)
                
            output.release()

if __name__ == "__main__":
    app = ScreenRecorderApp()
    app.mainloop()