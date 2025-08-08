import os
import re
import time
from deep_translator import GoogleTranslator
from multiprocessing import Pool, cpu_count

target_folder = "luci-app-passwall2/root/usr/share/passwall2"

translator = GoogleTranslator(source='zh-CN', target='en')

chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

def translate_file(file_path):
    print(f"Translating file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    def translate_match(match):
        try:
            return translator.translate(match.group(0))
        except Exception as e:
            print(f"Error translating text: {match.group(0)}. Skipping...")
            return match.group(0)

    translated_content = chinese_pattern.sub(translate_match, content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(translated_content)

def process_files(files):
    with Pool(cpu_count()) as pool:
        pool.map(translate_file, files)

if __name__ == "__main__":
    files_to_translate = []
    for root, _, files in os.walk(target_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.endswith((".txt", ".log", ".json", ".lua", ".sh")):
                files_to_translate.append(file_path)

    print(f"Found {len(files_to_translate)} files to translate.")
    process_files(files_to_translate)
    print("Translation completed.")
