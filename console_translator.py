from googletrans import Translator
import time

translator = Translator()

def translate_long_text(text, dest='ru', max_length=10000):
    sentences = text.split('. ')
    translated_parts = []
    
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                try:
                    translated = translator.translate(current_chunk, dest=dest)
                    translated_parts.append(translated.text)
                except Exception as e:
                    print(f"Ой.. ошибочка: {e}")
                    translated_parts.append(current_chunk)
                current_chunk = sentence + ". "
    
    if current_chunk:
        try:
            translated = translator.translate(current_chunk, dest=dest)
            translated_parts.append(translated.text)
        except Exception as e:
            print(f"Ой.. ошибочка: {e}")
            translated_parts.append(current_chunk)
    
    return " ".join(translated_parts)

def safe_translate(text, dest='ru', retries=3):
    for attempt in range(retries):
        try:
            if len(text) > 500:
                return translate_long_text(text, dest)
            else:
                result = translator.translate(text, dest=dest)
                return result.text
        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return f"[Ой.. ошибочка] {text}"

while True:
    try:
        text = input('Натапай что-н (не напишешь - я обижусь): ')
        if not text.strip():
            break
        
        print("Хммм...")
        translated = safe_translate(text)
        print(f'Воть: {translated}\n')
        
    except KeyboardInterrupt:
        print("\nФу таким быть")
        break
    except Exception as e:
        print(f"Ой.. ошибочка: {e}")