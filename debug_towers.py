"""Отладка загрузки башен"""
import pygame
import os

pygame.init()

towers_path = "assets/towers"

print("=" * 70)
print("TOWER LOADING DEBUG")
print("=" * 70)

for i in range(1, 9):
    tower_id = f"tower_{i}"
    tower_dir = os.path.join(towers_path, tower_id)
    
    print(f"\n{tower_id}:")
    print(f"  Directory: {tower_dir}")
    print(f"  Exists: {os.path.exists(tower_dir)}")
    
    if os.path.exists(tower_dir):
        # Показываем все файлы в папке
        files = os.listdir(tower_dir)
        print(f"  Files in folder: {files}")
        
        # Проверяем конкретный файл
        source = os.path.join(tower_dir, f"tower_{i}.png")
        print(f"  Looking for: tower_{i}.png")
        print(f"  Full path: {source}")
        print(f"  File exists: {os.path.exists(source)}")
        
        if os.path.exists(source):
            # Пробуем загрузить
            try:
                img = pygame.image.load(source)
                print(f"  ✓ Successfully loaded! Size: {img.get_width()}x{img.get_height()}")
            except Exception as e:
                print(f"  ✗ Failed to load: {e}")
        
        # Проверяем части
        for part in ['top', 'middle', 'base']:
            part_file = os.path.join(tower_dir, f"{part}.png")
            exists = os.path.exists(part_file)
            symbol = "✓" if exists else "✗"
            print(f"  {symbol} {part}.png: {exists}")

print("\n" + "=" * 70)
