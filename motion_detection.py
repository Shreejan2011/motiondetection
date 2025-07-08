import cv2
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk

class MotionDetectorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Motion Detector")
        
        self.cap = cv2.VideoCapture(0)
        
        self.label = tk.Label(master)
        self.label.pack()
        
        self.start_button = tk.Button(master, text="Start", command=self.start_motion_detection)
        self.start_button.pack(side=tk.LEFT)
        
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_motion_detection)
        self.stop_button.pack(side=tk.LEFT)
        
        self.running = False
        
    def start_motion_detection(self):
        self.running = True
        self.motion_detection()
        
    def stop_motion_detection(self):
        self.running = False
        
    def motion_detection(self):
        if self.running:
            _, frame1 = self.cap.read()
            frame1 = cv2.flip(frame1, 1)
            _, frame2 = self.cap.read()
            frame2 = cv2.flip(frame2, 1)

            diff = cv2.absdiff(frame2, frame1)
            diff = cv2.blur(diff, (5,5))
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, threshd = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(threshd, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            x = 300
            if contours:
                max_cnt = max(contours, key=cv2.contourArea)
                x,y,w,h = cv2.boundingRect(max_cnt)
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame1, "MOTION", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

            img = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            self.label.imgtk = img
            self.label.config(image=img)
            self.label.after(10, self.motion_detection)
        else:
            self.cap.release()

def main():
    root = tk.Tk()
    app = MotionDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
