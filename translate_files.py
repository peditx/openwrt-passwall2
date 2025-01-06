import os
import re
from googletrans import Translator

target_folder = "luci-app-passwall2/root/usr/share/passwall2"

translator = Translator()

chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

for root, _, files in os.walk(target_folder):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        if file_path.endswith((".txt", ".log", ".json", ".lua", ".sh")):  # بررسی پسوند فایل
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            def translate_match(match):
                try:
                    return translator.translate(match.group(0), src="zh-cn", dest="en").text
                except Exception as e:
                    print(f"Error translating text: {match.group(0)}. Skipping...")
                    return match.group(0)

            translated_content = chinese_pattern.sub(translate_match, content)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(translated_content)

print("Translation completed.")
