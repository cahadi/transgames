from tkinter import *
import pyautogui
import pytesseract
from PIL import Image
from pynput import keyboard
import threading

class ScreenTextRecognizer:
    def __init__(self):
        self.root = Tk()
        self.root.title(" Распознаватель Текста ")
        
        self.root.wait_visibility(self.root)
        self.root.wm_attributes("-alpha", 0.5)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        self.colors = {
            'bg_main': '#FFE4E6',
            'bg_frame': '#FFB7C5',
            'bg_text': '#FFF9FB',
            'accent': '#FF69B4',
            'text_dark': '#8B4789',
            'highlight': '#FFD1DC'
        }
        
        self.setup_ui()
        self.setup_global_hotkeys()
        
    def setup_ui(self):
        self.root.geometry("500x300+100+100")
        self.root.configure(bg=self.colors['bg_main'])
        
        self.main_frame = Frame(self.root, bg=self.colors['bg_frame'], relief=RAISED, bd=3,
                               highlightbackground=self.colors['accent'],
                               highlightthickness=2)
        self.main_frame.pack(fill=BOTH, expand=True, padx=8, pady=8)
        
        self.header_frame = Frame(self.main_frame, bg=self.colors['bg_frame'])
        self.header_frame.pack(fill=X, padx=10, pady=(10, 5))
        
        self.title_label = Label(self.header_frame, 
                                text=" Милый Распознаватель Текста ",
                                bg=self.colors['bg_frame'],
                                fg=self.colors['text_dark'],
                                font=("Comic Sans MS", 12, "bold"))
        self.title_label.pack()
        
        self.text_frame = Frame(self.main_frame, 
                               bg=self.colors['bg_text'],
                               relief=GROOVE, 
                               bd=3,
                               highlightbackground=self.colors['highlight'],
                               highlightthickness=1)
        self.text_frame.pack(fill=BOTH, expand=True, padx=12, pady=8)
        
        self.text_label = Label(self.text_frame, 
                               text=" Наведи курсор на текст и нажми F2! \n\n Я распознаю текст вокруг курсора ", 
                               bg=self.colors['bg_text'],
                               fg=self.colors['text_dark'],
                               wraplength=400, 
                               justify=CENTER,
                               font=("Segoe UI Emoji", 11),
                               padx=20,
                               pady=20)
        self.text_label.pack(fill=BOTH, expand=True)
        
        self.bottom_frame = Frame(self.main_frame, bg=self.colors['bg_frame'])
        self.bottom_frame.pack(fill=X, padx=10, pady=(5, 10))
        
        self.hotkeys_label = Label(self.bottom_frame, 
                                   text="F2: Распознать текст    Esc: Закрыть окошко", 
                                   bg=self.colors['bg_frame'],
                                   fg=self.colors['text_dark'],
                                   font=("Arial", 9, "bold"))
        self.hotkeys_label.pack()
    
    def setup_global_hotkeys(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f2:
                    self.root.after(0, self.capture_area_around_cursor)
                elif key == keyboard.Key.esc:
                    self.root.after(0, self.gentle_exit)
            except Exception as e:
                print(f"Ошибочка: {e}")
        
        def start_listener():
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        
        listener_thread = threading.Thread(target=start_listener, daemon=True)
        listener_thread.start()
        
    def gentle_exit(self):
        self.text_label.config(text="Пока-пока! Возвращайся скорее!")
        self.root.after(1000, self.root.quit)
        
    def capture_area_around_cursor(self):
        try:
            self.text_label.config(text="Ищу текст вокруг курсора...\n\n Одна секундочка!")
            self.root.update()

            x, y = pyautogui.position()
            region = (max(0, x-200), max(0, y-100), 400, 200)
            screenshot = pyautogui.screenshot(region=region)
            
            text = pytesseract.image_to_string(screenshot, lang='rus+eng')
            
            if text.strip():
                display_text = text.strip()[:400] + "..." if len(text) > 400 else text.strip()
                self.update_text(display_text)
            else:
                self.update_text("Текст не найден...\n\n Попробуй приблизиться к тексту!")
                
        except Exception as e:
            self.update_text(f"Ой-ой! Ошибка:\n{str(e)}\n\nПопробуй еще раз!")
    
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
        
        self.flash_accent()
    
    def flash_accent(self):
        original_bg = self.text_frame.cget('highlightbackground')
        
        def change_color(color):
            self.text_frame.config(highlightbackground=color)
        
        for i in range(3):
            self.root.after(i * 200, lambda: change_color(self.colors['accent']))
            self.root.after(i * 200 + 100, lambda: change_color(original_bg))
    

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.gentle_exit()

if __name__ == "__main__":
    app = ScreenTextRecognizer()
    app.run()