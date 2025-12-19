from tkinter import *
import pyautogui
import pytesseract
from PIL import Image
from pynput import keyboard
import threading

class ScreenTextRecognizer:
    def __init__(self):
        self.root = Tk()
        self.root.title("Распознавание текста")
        
        self.root.wait_visibility(self.root)
        self.root.wm_attributes("-alpha", 0.4)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        self.setup_ui()
        self.setup_global_hotkeys()
        
    def setup_ui(self):
        self.root.geometry("500x300+100+100")
        
        self.main_frame = Frame(self.root, bg='#2E8B57', relief=RAISED, bd=3)
        self.main_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        self.text_frame = Frame(self.main_frame, bg='white', relief=SUNKEN, bd=2)
        self.text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.text_label = Label(self.text_frame, text="Нажмите F2 для распознавания текста", 
                               bg='white', wraplength=400, justify=LEFT,
                               font=("Arial", 11))
        self.text_label.pack(pady=15, padx=15, fill=BOTH, expand=True)
        
        self.hotkeys_frame = Frame(self.main_frame, bg='#2E8B57')
        self.hotkeys_frame.pack(anchor=SE, padx=5, pady=5)
        
        self.hotkeys_label = Label(self.hotkeys_frame, 
                                   text="F2:Распознать  Esc:Выход", 
                                   bg='#2E8B57', fg='white', 
                                   font=("Arial", 8, "bold"))
        self.hotkeys_label.pack()
        
    def setup_global_hotkeys(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f2:
                    self.root.after(0, self.capture_area_around_cursor)
                elif key == keyboard.Key.esc:
                    self.root.after(0, self.root.quit)
            except Exception as e:
                print(f"Ошибка: {e}")
        
        def start_listener():
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        
        listener_thread = threading.Thread(target=start_listener, daemon=True)
        listener_thread.start()
        
    def capture_area_around_cursor(self):
        try:
            x, y = pyautogui.position()
            region = (max(0, x-200), max(0, y-100), 400, 200)
            screenshot = pyautogui.screenshot(region=region)
            
            text = pytesseract.image_to_string(screenshot, lang='rus+eng')
            
            if text.strip():
                display_text = text.strip()[:400] + "..." if len(text) > 400 else text.strip()
                self.update_text(display_text)
            else:
                self.update_text("Текст не распознан")
                
        except Exception as e:
            self.update_text(f"Ошибка: {str(e)}")
    
    def update_text(self, text):
        if len(text) > 500:
            text = text[:500] + "..."
        
        formatted_text = text.replace('\n', ' ').strip()
        if len(formatted_text) > 100:
            words = formatted_text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 60:
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            formatted_text = '\n'.join(lines)
        
        self.text_label.config(text=formatted_text)
    
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

if __name__ == "__main__":
    app = ScreenTextRecognizer()
    app.run()