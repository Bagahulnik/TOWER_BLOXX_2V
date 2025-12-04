"""Скрипт для разделения всех башен"""
import pygame
import os

pygame.init()

towers_path = "assets/towers"
block_size = 64

print("=" * 70)
print("SPLITTING TOWER SPRITES")
print("=" * 70)

for i in range(1, 9):
    tower_id = f"tower_{i}"
    tower_dir = os.path.join(towers_path, tower_id)
    source_file = os.path.join(tower_dir, f"tower_{i}.png")
    
    if not os.path.exists(source_file):
        print(f"\n{tower_id}: File not found, skipping")
        continue
    
    print(f"\n{tower_id}:")
    print(f"  Loading: {source_file}")
    
    try:
        # Загружаем изображение
        img = pygame.image.load(source_file)
        width = img.get_width()
        height = img.get_height()
        
        print(f"  Size: {width}x{height}")
        
        num_blocks = height // block_size
        print(f"  Blocks: {num_blocks}")
        
        # Верхний блок
        top = pygame.Surface((width, block_size), pygame.SRCALPHA)
        top.blit(img, (0, 0), (0, 0, width, block_size))
        top_path = os.path.join(tower_dir, "top.png")
        pygame.image.save(top, top_path)
        print(f"  ✓ Saved: top.png")
        
        # Средний блок
        middle = pygame.Surface((width, block_size), pygame.SRCALPHA)
        middle.blit(img, (0, 0), (0, block_size, width, block_size))
        middle_path = os.path.join(tower_dir, "middle.png")
        pygame.image.save(middle, middle_path)
        print(f"  ✓ Saved: middle.png")
        
        # Нижний блок
        base_y = height - block_size
        base = pygame.Surface((width, block_size), pygame.SRCALPHA)
        base.blit(img, (0, 0), (0, base_y, width, block_size))
        base_path = os.path.join(tower_dir, "base.png")
        pygame.image.save(base, base_path)
        print(f"  ✓ Saved: base.png")
        
        # Полное изображение
        full_path = os.path.join(tower_dir, "full.png")
        pygame.image.save(img, full_path)
        print(f"  ✓ Saved: full.png")
        
        print(f"  ✓ {tower_id} complete!")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "=" * 70)
print("✓ ALL DONE! Now run your game: python main.py")
print("=" * 70)
