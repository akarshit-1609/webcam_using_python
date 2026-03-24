import cv2
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

class WebcamTk:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.exist = True
        else:
            self.exist = False
        self.frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.camera = tk.Toplevel()
        self.size = 0.2
        self.width, self.height = int(self.frame_width*self.size), int(self.frame_height*self.size)
        self.corner_radius = 20
        self.bg_color = '#abcdef'
        self.camera.overrideredirect(True)
        self.camera.attributes("-topmost", True)
        self.camera.wm_attributes("-transparentcolor", self.bg_color)
        self.camera.config(bg=self.bg_color, cursor="hand2")
        screen_w = self.camera.winfo_screenwidth()
        screen_h = self.camera.winfo_screenheight()
        x = screen_w - self.width - 20
        y = screen_h - self.height - 40 
        self.camera.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.label = tk.Label(self.camera, bg=self.bg_color)
        self.label.pack()
        self.running = False
        self.rectangular = True
        self.flipped = True
        self.mask = self.get_rounded_mask((self.width, self.height))
        self.camera.bind("<Button-1>", self.start_drag)
        self.camera.bind("<B1-Motion>", self.do_drag)

    def get_rounded_mask(self, size):
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, size[0], size[1]), radius=self.corner_radius, fill=255)
        return mask
    
    def get_circular_mask(self, size):
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        return mask

    def start_drag(self, event):
        self._start_x = event.x_root
        self._start_y = event.y_root
        self._win_x = self.camera.winfo_x()
        self._win_y = self.camera.winfo_y()

    def do_drag(self, event):
        delta_x = event.x_root -self._start_x
        delta_y = event.y_root -self._start_y
        new_x = self._win_x + delta_x
        new_y = self._win_y + delta_y
        self.camera.geometry(f"+{new_x}+{new_y}")

    def update_frame(self):
        if not self.running:
            if self.exist:
                return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if not self.flipped:
                frame = cv2.flip(frame, 1)
            img = Image.fromarray(frame)
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            mask = self.mask
            final_img = Image.new("RGB", (self.width, self.height), self.bg_color)
            final_img.paste(img, (0, 0), mask=mask)
            self.tk_img = ImageTk.PhotoImage(final_img)
            self.label.config(image=self.tk_img)
        self.camera.after(10, self.update_frame)

    def set_flipped(self, flipped):
        self.flipped = flipped

    def startWebcam(self):
        if not self.running:
            self.camera.deiconify()
            self.running = True
            self.cap = cv2.VideoCapture(0)
            self.update_frame()

    def stopWebcam(self):
        if self.running:
            self.running = False
            if self.cap:
                self.cap.release()
            self.camera.withdraw()
    
    def set_border_radius(self, n):
        self.corner_radius = n
        if self.rectangular:
            self.mask = self.get_rounded_mask((self.width, self.height))
    
    def set_size(self, size):
        self.size = size
        width = int(self.frame_width*self.size)
        if self.rectangular:
            self.width, self.height = int(self.frame_width*self.size), int(self.frame_height*self.size)
        else:
            self.width, self.height = int(self.frame_height*self.size), int(self.frame_height*self.size)
        self.camera.update_idletasks()
        self.camera.geometry(f"{width}x{self.height}+{self.camera.winfo_x()}+{self.camera.winfo_y()}")
        if self.rectangular:
            self.mask = self.get_rounded_mask((self.width, self.height))
        else:
            self.mask = self.get_circular_mask((self.width, self.height))
    
    def set_rectangular(self):
        if not self.rectangular:
            self.rectangular = True
            self.width, self.height = int(self.frame_width*self.size), int(self.frame_height*self.size)
            self.mask = self.get_rounded_mask((self.width, self.height))

    def set_circular(self):
        if self.rectangular:
            self.rectangular = False
            self.width, self.height = int(self.frame_height*self.size), int(self.frame_height*self.size)
            self.mask = self.get_circular_mask((self.width, self.height))


if __name__ == "__main__":
    def start(event):
        app.startWebcam()
    def stop(event):
        app.stopWebcam()
    root = tk.Tk()
    root.title("Camera Test")
    root.geometry("300x100+100+100")
    app = WebcamTk()
    root.bind("<Return>", start)
    root.bind("<Escape>", stop)
    root.mainloop()
