"""Точка входа в игру с автоматической проверкой ресурсов"""
import pygame
import os
import sys


def check_and_prepare_resources():
    """Проверка и подготовка всех ресурсов перед запуском игры"""
    print("\n" + "=" * 70)
    print("TOWER BROCKS - RESOURCE CHECKER")
    print("=" * 70)
    
    # Инициализируем pygame для работы со спрайтами
    pygame.init()
    
    # 1. Проверка структуры папок
    print("\n[1/4] Checking folder structure...")
    required_folders = [
        "assets",
        "assets/towers",
        "assets/audio",
        "assets/backgrounds",
        "core",
        "entities",
        "managers",
        "ui"
    ]
    
    missing_folders = []
    for folder in required_folders:
        if not os.path.exists(folder):
            missing_folders.append(folder)
            print(f"  ✗ Missing: {folder}")
        else:
            print(f"  ✓ Found: {folder}")
    
    if missing_folders:
        print(f"\n⚠ Warning: {len(missing_folders)} folders missing")
        for folder in missing_folders:
            os.makedirs(folder, exist_ok=True)
            print(f"  Created: {folder}")
    
    # 2. Проверка наличия частей башен
    print("\n[2/4] Checking tower parts...")
    towers_path = "assets/towers"
    complete_towers = 0
    
    for i in range(1, 9):
        tower_id = f"tower_{i}"
        tower_dir = os.path.join(towers_path, tower_id)
        
        if not os.path.exists(tower_dir):
            os.makedirs(tower_dir, exist_ok=True)
            print(f"  ✗ {tower_id}: Folder created, missing parts")
            continue
        
        # Проверяем новые файлы: bot + mid_0/1/2/3
        required_parts = [
            f"tower_{i}_bot.png",
            f"tower_{i}_mid_0.png",
            f"tower_{i}_mid_1.png",
            f"tower_{i}_mid_2.png",
            f"tower_{i}_mid_3.png"
        ]
        
        missing_parts = []
        for part in required_parts:
            if not os.path.exists(os.path.join(tower_dir, part)):
                missing_parts.append(part)
        
        if not missing_parts:
            complete_towers += 1
            print(f"  ✓ {tower_id}: All 5 parts found")
        else:
            print(f"  ⚠ {tower_id}: Missing {len(missing_parts)} parts")
    
    print(f"\nComplete towers: {complete_towers}/8")
    
    # 3. Проверка фонов
    print("\n[3/4] Checking backgrounds...")
    backgrounds_path = "assets/backgrounds"
    backgrounds_found = 0
    
    for i in range(1, 4):  # bg1, bg2, bg3
        bg_file = os.path.join(backgrounds_path, f"bg{i}.png")
        if os.path.exists(bg_file):
            backgrounds_found += 1
            print(f"  ✓ bg{i}.png found")
        else:
            print(f"  ✗ bg{i}.png not found")
    
    print(f"\nBackgrounds found: {backgrounds_found}/3")
    
    # 4. Проверка аудио
    print("\n[4/4] Checking audio files...")
    audio_path = "assets/audio"
    audio_files = ["music.mp3", "build.wav", "fall.wav", "gold.wav"]
    audio_found = 0
    
    for audio_file in audio_files:
        if os.path.exists(os.path.join(audio_path, audio_file)):
            audio_found += 1
            print(f"  ✓ {audio_file} found")
        else:
            print(f"  ⚠ {audio_file} not found")
    
    print(f"\nAudio files found: {audio_found}/{len(audio_files)}")
    
    # Финальный статус
    print("\n" + "=" * 70)
    if complete_towers >= 1:
        print(f"✓ RESOURCE CHECK COMPLETE - {complete_towers}/8 TOWERS READY")
        print("=" * 70 + "\n")
        return True
    else:
        print("✗ NO VALID TOWERS FOUND")
        print("=" * 70)
        print("\nPlease add tower parts to:")
        print("  assets/towers/tower_1/tower_1_bot.png")
        print("  assets/towers/tower_1/tower_1_mid_0.png")
        print("  assets/towers/tower_1/tower_1_mid_1.png")
        print("  assets/towers/tower_1/tower_1_mid_2.png")
        print("  assets/towers/tower_1/tower_1_mid_3.png")
        print("  ... etc")
        print("\nGame will use fallback sprites.")
        print("=" * 70 + "\n")
        
        response = input("Continue anyway? (y/n): ").lower()
        return response == 'y'


if __name__ == "__main__":
    try:
        # Автоматическая проверка и подготовка ресурсов
        if not check_and_prepare_resources():
            print("Exiting...")
            sys.exit(0)
        
        # Запуск игры
        from core.game import Game
        game = Game()
        game.run()
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user")
        sys.exit(0)
    except Exception as e:
        print("\n" + "=" * 70)
        print("ERROR OCCURRED")
        print("=" * 70)
        print(f"\n{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 70)
        input("\nPress Enter to exit...")
        sys.exit(1)
