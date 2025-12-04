"""Автоматическое разделение спрайтов башен на части (только Pygame)"""
import pygame
import os

class SpriteSplitter:
    def __init__(self, towers_path="assets/towers", block_size=64):
        self.towers_path = towers_path
        self.block_size = block_size
    
    def split_tower(self, tower_id, source_image_path):
        """
        Разделяет полный спрайт башни на 3 части:
        - top.png (верхний блок)
        - middle.png (средний повторяющийся блок)
        - base.png (нижний блок)
        """
        try:
            # Открываем изображение через Pygame
            img = pygame.image.load(source_image_path)
            width = img.get_width()
            height = img.get_height()
            
            # Определяем количество блоков
            num_blocks = height // self.block_size
            
            # Создаем директорию для башни
            tower_dir = os.path.join(self.towers_path, tower_id)
            os.makedirs(tower_dir, exist_ok=True)
            
            # Сохраняем полное изображение
            full_path = os.path.join(tower_dir, "full.png")
            pygame.image.save(img, full_path)
            
            if num_blocks >= 3:
                # Верхний блок (top) - первый блок сверху
                top = pygame.Surface((width, self.block_size), pygame.SRCALPHA)
                top.blit(img, (0, 0), (0, 0, width, self.block_size))
                top_path = os.path.join(tower_dir, "top.png")
                pygame.image.save(top, top_path)
                
                # Средний блок (middle) - второй блок сверху
                middle = pygame.Surface((width, self.block_size), pygame.SRCALPHA)
                middle.blit(img, (0, 0), (0, self.block_size, width, self.block_size))
                middle_path = os.path.join(tower_dir, "middle.png")
                pygame.image.save(middle, middle_path)
                
                # Нижний блок (base) - последний блок снизу
                base_y = height - self.block_size
                base = pygame.Surface((width, self.block_size), pygame.SRCALPHA)
                base.blit(img, (0, 0), (0, base_y, width, self.block_size))
                base_path = os.path.join(tower_dir, "base.png")
                pygame.image.save(base, base_path)
                
            elif num_blocks >= 2:
                # Если только 2 блока
                top = pygame.Surface((width, self.block_size), pygame.SRCALPHA)
                top.blit(img, (0, 0), (0, 0, width, self.block_size))
                pygame.image.save(top, os.path.join(tower_dir, "top.png"))
                
                middle = pygame.Surface((width, self.block_size), pygame.SRCALPHA)
                middle.blit(img, (0, 0), (0, self.block_size, width, self.block_size))
                pygame.image.save(middle, os.path.join(tower_dir, "middle.png"))
                
                # Base используем тот же что и middle
                pygame.image.save(middle, os.path.join(tower_dir, "base.png"))
                
            else:
                # Если башня слишком короткая - используем один блок для всех
                block_height = min(self.block_size, height)
                single = pygame.Surface((width, block_height), pygame.SRCALPHA)
                single.blit(img, (0, 0), (0, 0, width, block_height))
                pygame.image.save(single, os.path.join(tower_dir, "top.png"))
                pygame.image.save(single, os.path.join(tower_dir, "middle.png"))
                pygame.image.save(single, os.path.join(tower_dir, "base.png"))
            
            return True
            
        except Exception as e:
            print(f"Error splitting tower {tower_id}: {str(e)}")
            return False
    
    def split_all_towers(self):
        """
        Автоматически находит и разделяет все спрайты башен
        Ищет файлы tower_X.jpg или tower_X.png в папках towers
        """
        tower_formats = ['.jpg', '.jpeg', '.png']
        towers_processed = 0
        
        for i in range(1, 9):  # tower_1 до tower_8
            tower_id = f"tower_{i}"
            tower_dir = os.path.join(self.towers_path, tower_id)
            
            # Проверяем существование директории
            if not os.path.exists(tower_dir):
                continue
            
            # Ищем исходный файл
            source_file = None
            for ext in tower_formats:
                potential_path = os.path.join(tower_dir, f"{tower_id}{ext}")
                if os.path.exists(potential_path):
                    source_file = potential_path
                    break
            
            if source_file:
                print(f"Processing {tower_id}...")
                if self.split_tower(tower_id, source_file):
                    towers_processed += 1
                    print(f"  ✓ {tower_id} split successfully")
            else:
                # Проверяем, может части уже существуют
                parts_exist = all([
                    os.path.exists(os.path.join(tower_dir, f"{part}.png"))
                    for part in ['top', 'middle', 'base']
                ])
                if parts_exist:
                    print(f"  ✓ {tower_id} parts already exist")
                else:
                    print(f"  ⚠ {tower_id} source not found in {tower_dir}")
        
        if towers_processed > 0:
            print(f"\nTotal towers processed: {towers_processed}")
        return towers_processed
