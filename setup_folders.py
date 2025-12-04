# setup_folders.py
import os

# Создаем структуру папок
folders = [
    "assets",
    "assets/audio",
    "assets/backgrounds",
    "assets/towers",
    "assets/towers/tower_1",
    "assets/towers/tower_2",
    "assets/towers/tower_3",
    "assets/towers/tower_4",
    "assets/towers/tower_5",
    "assets/towers/tower_6",
    "assets/towers/tower_7",
    "assets/towers/tower_8",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✓ Created: {folder}")

print("\n✅ Folder structure created!")
print("\nNow place your files:")
print("  - Audio files (bgm.wav, fall.wav, etc.) → assets/audio/")
print("  - Background images (bg1.png - bg5.png) → assets/backgrounds/")
print("  - Tower sprites (tower_X.jpg) → assets/towers/tower_X/")
print("  - ground_tileset.png → assets/")
