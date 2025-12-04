# split_towers_96px.py
"""Скрипт для разделения башен с шириной 96px"""
import pygame
import os

pygame.init()

towers_path = "assets/towers"
block_width = 96  # ЕЩЕ ШИРЕ
block_height = 64

print("=" * 70)
print("SPLITTING TOWER SPRITES (96px width)")
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
        original_width = img.get_width()
        original_height = img.get_height()
        
        print(f"  Original size: {original_width}x{original_height}")
        
        # Растягиваем ширину до 96px
        if original_width != block_width:
            scale_factor = block_width / original_width
            new_height = int(original_height * scale_factor)
            img = pygame.transform.scale(img, (block_width, new_height))
            print(f"  Scaled to: {block_width}x{new_height}")
        
        width = img.get_width()
        height = img.get_height()
        
        num_blocks = height // block_height
        print(f"  Blocks: {num_blocks}")
        
        # Верхний блок
        top = pygame.Surface((width, block_height), pygame.SRCALPHA)
        top.blit(img, (0, 0), (0, 0, width, block_height))
        top_path = os.path.join(tower_dir, "top.png")
        pygame.image.save(top, top_path)
        print(f"  ✓ Saved: top.png")
        
        # Средний блок
        middle = pygame.Surface((width, block_height), pygame.SRCALPHA)
        middle.blit(img, (0, 0), (0, block_height, width, block_height))
        middle_path = os.path.join(tower_dir, "middle.png")
        pygame.image.save(middle, middle_path)
        print(f"  ✓ Saved: middle.png")
        
        # Нижний блок
        base_y = height - block_height
        base = pygame.Surface((width, block_height), pygame.SRCALPHA)
        base.blit(img, (0, 0), (0, base_y, width, block_height))
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
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print("✓ ALL DONE! Blocks are now 96px wide")
print("✓ Run your game: python main.py")
print("=" * 70)
