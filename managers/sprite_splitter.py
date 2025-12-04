"""Автоматическое разделение спрайтов башен на части (только Pygame)"""
import pygame
import os

class SpriteSplitter:
    def __init__(self, towers_path="assets/towers", block_size=64):
        self.towers_path = towers_path
        self.block_width = 96  # БЫЛО 80, ТЕПЕРЬ 96
        self.block_height = 64
        self.block_size = block_size
    pygame.init()
    
    def split_tower(self, tower_id, source_image_path):
        """
        Разделяет полный спрайт башни на 3 части:
        - top.png (верхний блок)
        - middle.png (средний повторяющийся блок)
        - base.png (нижний блок)
        """
        try:
            print(f"    Loading image from: {source_image_path}")
            
            # Открываем изображение через Pygame
            img = pygame.image.load(source_image_path)
            original_width = img.get_width()
            original_height = img.get_height()
            
            print(f"    Original size: {original_width}x{original_height}")
            
            # Масштабируем до нужной ширины (80px)
            if original_width != self.block_width:
                scale_factor = self.block_width / original_width
                new_height = int(original_height * scale_factor)
                img = pygame.transform.scale(img, (self.block_width, new_height))
                print(f"    Scaled to: {self.block_width}x{new_height}")
            
            width = img.get_width()
            height = img.get_height()
            
            # Определяем количество блоков
            num_blocks = height // self.block_height
            print(f"    Number of blocks: {num_blocks}")
            
            # Создаем директорию для башни
            tower_dir = os.path.join(self.towers_path, tower_id)
            os.makedirs(tower_dir, exist_ok=True)
            
            # Сохраняем полное изображение
            full_path = os.path.join(tower_dir, "full.png")
            pygame.image.save(img, full_path)
            print(f"    Saved full.png")
            
            if num_blocks >= 3:
                # Верхний блок (top) - первый блок сверху
                top = pygame.Surface((width, self.block_height), pygame.SRCALPHA)
                top.blit(img, (0, 0), (0, 0, width, self.block_height))
                top_path = os.path.join(tower_dir, "top.png")
                pygame.image.save(top, top_path)
                print(f"    Saved top.png")
                
                # Средний блок (middle) - второй блок сверху
                middle = pygame.Surface((width, self.block_height), pygame.SRCALPHA)
                middle.blit(img, (0, 0), (0, self.block_height, width, self.block_height))
                middle_path = os.path.join(tower_dir, "middle.png")
                pygame.image.save(middle, middle_path)
                print(f"    Saved middle.png")
                
                # Нижний блок (base) - последний блок снизу
                base_y = height - self.block_height
                base = pygame.Surface((width, self.block_height), pygame.SRCALPHA)
                base.blit(img, (0, 0), (0, base_y, width, self.block_height))
                base_path = os.path.join(tower_dir, "base.png")
                pygame.image.save(base, base_path)
                print(f"    Saved base.png")
                
            elif num_blocks >= 2:
                # Если только 2 блока
                top = pygame.Surface((width, self.block_height), pygame.SRCALPHA)
                top.blit(img, (0, 0), (0, 0, width, self.block_height))
                pygame.image.save(top, os.path.join(tower_dir, "top.png"))
                
                middle = pygame.Surface((width, self.block_height), pygame.SRCALPHA)
                middle.blit(img, (0, 0), (0, self.block_height, width, self.block_height))
                pygame.image.save(middle, os.path.join(tower_dir, "middle.png"))
                
                # Base используем тот же что и middle
                pygame.image.save(middle, os.path.join(tower_dir, "base.png"))
                print(f"    Saved all parts (2 blocks)")
                
            else:
                # Если башня слишком короткая - используем один блок для всех
                block_height = min(self.block_height, height)
                single = pygame.Surface((width, block_height), pygame.SRCALPHA)
                single.blit(img, (0, 0), (0, 0, width, block_height))
                pygame.image.save(single, os.path.join(tower_dir, "top.png"))
                pygame.image.save(single, os.path.join(tower_dir, "middle.png"))
                pygame.image.save(single, os.path.join(tower_dir, "base.png"))
                print(f"    Saved all parts (1 block)")
            
            return True
            
        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def split_all_towers(self):
        """
        Автоматически находит и разделяет все спрайты башен
        Ищет файлы tower_X.png в папках towers
        """
        towers_processed = 0
        
        print(f"\nSearching for tower sprites in: {self.towers_path}")
        print(f"Target block size: {self.block_width}x{self.block_height}")
        print("-" * 60)
        
        for i in range(1, 9):  # tower_1 до tower_8
            tower_id = f"tower_{i}"
            tower_dir = os.path.join(self.towers_path, tower_id)
            
            print(f"\n{tower_id}:")
            
            # Проверяем существование директории
            if not os.path.exists(tower_dir):
                print(f"  ✗ Directory not found: {tower_dir}")
                continue
            
            # Показываем что есть в папке
            try:
                files = os.listdir(tower_dir)
                print(f"  Files in folder: {files}")
            except:
                pass
            
            # ГЛАВНОЕ: ищем именно tower_X.png
            source_file = os.path.join(tower_dir, f"tower_{i}.png")
            print(f"  Looking for: {source_file}")
            print(f"  File exists: {os.path.exists(source_file)}")
            
            if os.path.exists(source_file):
                print(f"  Processing tower_{i}.png...")
                if self.split_tower(tower_id, source_file):
                    towers_processed += 1
                    print(f"  ✓ Successfully split")
            else:
                # Проверяем, может части уже существуют
                parts_exist = all([
                    os.path.exists(os.path.join(tower_dir, f"{part}.png"))
                    for part in ['top', 'middle', 'base']
                ])
                if parts_exist:
                    print(f"  ✓ Split parts already exist")
                else:
                    print(f"  ⚠ No source file and no split parts found")
        
        print("\n" + "-" * 60)
        if towers_processed > 0:
            print(f"✓ Total towers processed: {towers_processed}")
        else:
            print(f"⚠ No towers were processed")
        
        return towers_processed
