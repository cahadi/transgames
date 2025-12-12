from tkinter import *
import pyautogui
import pytesseract
from PIL import Image
from pynput import keyboard
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from updated_translator import set_text_from_recognizer, translate_shared_text, auto_translate_recognized_text
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("translator", "translator.py")
    translator_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(translator_module)
    set_text_from_recognizer = translator_module.set_text_from_recognizer
    translate_shared_text = translator_module.translate_shared_text
    auto_translate_recognized_text = translator_module.auto_translate_recognized_text

class ScreenTextRecognizer:
    def __init__(self):
        self.root = Tk()
        self.root.title("Это не игры трансов, а переводчик для игр")
        
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
            'highlight': '#FFD1DC',
            'translate_btn': '#FFD700'
        }
        
        self.recognized_text = ""
        
        self.setup_ui()
        self.setup_global_hotkeys()
        
    def setup_ui(self):
        self.root.geometry("500x350+100+100")
        self.root.configure(bg=self.colors['bg_main'])
        
        self.main_frame = Frame(self.root, bg=self.colors['bg_frame'], relief=RAISED, bd=3,
                               highlightbackground=self.colors['accent'],
                               highlightthickness=2)
        self.main_frame.pack(fill=BOTH, expand=True, padx=8, pady=8)
        
        self.header_frame = Frame(self.main_frame, bg=self.colors['bg_frame'])
        self.header_frame.pack(fill=X, padx=10, pady=(10, 5))
        
        self.title_label = Label(self.header_frame, 
                                text="Ми-ми-ми",
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
                               text="Наведи курсор на текст и нажми F2!\n\nТогда будет тот же текст, что ты и так видишь\n\nХа-ха", 
                               bg=self.colors['bg_text'],
                               fg=self.colors['text_dark'],
                               wraplength=400, 
                               justify=CENTER,
                               font=("Segoe UI Emoji", 11),
                               padx=20,
                               pady=20)
        self.text_label.pack(fill=BOTH, expand=True)
        
        self.translate_frame = Frame(self.main_frame, bg=self.colors['bg_frame'])
        self.translate_frame.pack(fill=X, padx=20, pady=5)
        
        self.bottom_frame = Frame(self.main_frame, bg=self.colors['bg_frame'])
        self.bottom_frame.pack(fill=X, padx=10, pady=(5, 10))
        
        self.hotkeys_label = Label(self.bottom_frame, 
                                   text="F1:Отстань  F2:Распознать  F3:Перевести  F4:Выход", 
                                   bg=self.colors['bg_frame'],
                                   fg=self.colors['text_dark'],
                                   font=("Arial", 8, "bold"))
        self.hotkeys_label.pack()
    
    def setup_global_hotkeys(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f2:
                    self.root.after(0, self.capture_area_around_cursor)
                elif key == keyboard.Key.f3:
                    self.root.after(0, self.translate_recognized_text)
                elif key == keyboard.Key.f4:
                    self.root.after(0, self.gentle_exit)
                elif key == keyboard.Key.f1:
                    self.text_label.config(text="Ха-ха-ха. Сам отстань -_-")
            except Exception as e:
                print(f"Ошибочка: {e}")
        
        def start_listener():
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        
        listener_thread = threading.Thread(target=start_listener, daemon=True)
        listener_thread.start()
        
    def gentle_exit(self):
        self.text_label.config(text="Пока-пока! Учи английский :3")
        self.root.after(1000, self.root.quit)
        
    def capture_area_around_cursor(self):
        try:
            self.text_label.config(text="Ищу текст вокруг курсора...\n\nОдна секундочка!")
            self.root.update()

            x, y = pyautogui.position()
            region = (max(0, x-200), max(0, y-100), 400, 200)
            screenshot = pyautogui.screenshot(region=region)
            
            text = pytesseract.image_to_string(screenshot, lang='rus+eng')
            
            if text.strip():
                self.recognized_text = text.strip()
                display_text = self.recognized_text[:400] + "..." if len(self.recognized_text) > 400 else self.recognized_text
                self.update_text(display_text)
                
                set_text_from_recognizer(self.recognized_text)
                print(f"Текст отправлен в переводчик: {self.recognized_text}")
            else:
                self.recognized_text = ""
                self.update_text("Текст не найден...\n\nДавай ближе")
                
        except Exception as e:
            self.update_text(f"Ой-ой! Ошибка:\n{str(e)}\n\nПопробуй еще раз!")
    
    def translate_recognized_text(self):
        if not self.recognized_text.strip():
            self.update_text("Сначала распознай текст (F2)!")
            return
        
        try:
            self.text_label.config(text="Перевожу текст...\n\nПодожди немного!")
            self.root.update()
            
            translated = translate_shared_text()
            
            if translated:
                self.update_text(f"Вот те перевод:\n{translated}")
            else:
                self.update_text("Не удалось перевести текст\n\nПопробуй еще раз!")
                
        except Exception as e:
            self.update_text(f"Ошибка перевода:\n{str(e)}")
    
    def update_text(self, text):
        if len(text) > 500:
            text = text[:500] + "..."
        
        formatted_text = ' '.join(text.split())
        formatted_text = formatted_text.strip()
        
        if len(formatted_text) > 60:
            lines = []
            current_line = ""
            
            for word in formatted_text.split():
                test_line = current_line + " " + word if current_line else word
                if len(test_line) <= 60:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            formatted_text = '\n'.join(lines)
        else:
            formatted_text = formatted_text
        
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