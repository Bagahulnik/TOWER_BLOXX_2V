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
    
    # 2. Проверка наличия исходных спрайтов башен
    print("\n[2/4] Checking tower source sprites...")
    towers_path = "assets/towers"
    towers_found = 0
    towers_missing = []
    
    for i in range(1, 9):
        tower_id = f"tower_{i}"
        tower_dir = os.path.join(towers_path, tower_id)
        
        if not os.path.exists(tower_dir):
            os.makedirs(tower_dir, exist_ok=True)
            towers_missing.append(tower_id)
            continue
        
        source_file = os.path.join(tower_dir, f"tower_{i}.png")
        if os.path.exists(source_file):
            towers_found += 1
            print(f"  ✓ {tower_id}: tower_{i}.png found")
        else:
            towers_missing.append(tower_id)
            print(f"  ✗ {tower_id}: tower_{i}.png not found")
    
    print(f"\nTowers found: {towers_found}/8")
    
    if towers_missing:
        print(f"⚠ Missing towers: {', '.join(towers_missing)}")
        print("  These towers will use fallback sprites")
    
    # 3. Разделение спрайтов башен
    print("\n[3/4] Splitting tower sprites...")
    from managers.sprite_splitter import SpriteSplitter
    
    splitter = SpriteSplitter("assets/towers", 64)
    processed = splitter.split_all_towers()
    
    if processed > 0:
        print(f"✓ Processed {processed} towers")
    else:
        print("ℹ All tower parts already exist or no source files found")
    
    # 4. Проверка наличия разделенных частей
    print("\n[4/4] Verifying tower parts...")
    complete_towers = 0
    
    for i in range(1, 9):
        tower_id = f"tower_{i}"
        tower_dir = os.path.join(towers_path, tower_id)
        
        if not os.path.exists(tower_dir):
            continue
        
        parts_exist = all([
            os.path.exists(os.path.join(tower_dir, f"{part}.png"))
            for part in ['top', 'middle', 'base']
        ])
        
        if parts_exist:
            complete_towers += 1
            print(f"  ✓ {tower_id}: All parts ready")
        else:
            missing_parts = [
                part for part in ['top', 'middle', 'base']
                if not os.path.exists(os.path.join(tower_dir, f"{part}.png"))
            ]
            print(f"  ⚠ {tower_id}: Missing parts: {', '.join(missing_parts)}")
    
    print(f"\nComplete towers: {complete_towers}/8")
    
    # Финальный статус
    print("\n" + "=" * 70)
    if complete_towers >= 1:
        print("✓ RESOURCE CHECK COMPLETE - STARTING GAME")
        print("=" * 70 + "\n")
        return True
    else:
        print("✗ NO VALID TOWERS FOUND")
        print("=" * 70)
        print("\nPlease add tower sprites to:")
        print("  assets/towers/tower_1/tower_1.png")
        print("  assets/towers/tower_2/tower_2.png")
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
