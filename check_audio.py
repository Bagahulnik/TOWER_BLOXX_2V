# check_audio.py
import os

audio_path = "assets/audio"

print("Checking audio files in:", audio_path)
print("=" * 60)

if os.path.exists(audio_path):
    files = os.listdir(audio_path)
    print(f"Found {len(files)} files:")
    for file in files:
        full_path = os.path.join(audio_path, file)
        size = os.path.getsize(full_path)
        print(f"  - {file} ({size} bytes)")
else:
    print("Audio folder not found!")

print("=" * 60)

# Проверяем конкретные файлы
required_files = ['bgm.wav', 'build.wav', 'gold.wav', 'overmusic.wav', 'fall.wav']
print("\nRequired files check:")
for file in required_files:
    path = os.path.join(audio_path, file)
    exists = "✓" if os.path.exists(path) else "✗"
    print(f"{exists} {file}")
