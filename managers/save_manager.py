"""Менеджер сохранений"""
import json
import os

class SaveManager:
    def __init__(self, save_file="save_data.json"):
        self.save_file = save_file
        self.data = self.load_data()
    
    def load_data(self):
        """Загрузка данных из файла"""
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                return json.load(f)
        return {
            'coins': 0,
            'high_score': 0,
            'unlocked_skins': ['tower_1'],
            'selected_skin': 'tower_1'
        }
    
    def save_data(self):
        """Сохранение данных в файл"""
        with open(self.save_file, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def add_coins(self, amount):
        """Добавить монеты"""
        self.data['coins'] += amount
        self.save_data()
    
    def spend_coins(self, amount):
        """Потратить монеты"""
        if self.data['coins'] >= amount:
            self.data['coins'] -= amount
            self.save_data()
            return True
        return False
    
    def unlock_skin(self, skin_id):
        """Разблокировать скин"""
        if skin_id not in self.data['unlocked_skins']:
            self.data['unlocked_skins'].append(skin_id)
            self.save_data()
    
    def set_selected_skin(self, skin_id):
        """Выбрать скин"""
        if skin_id in self.data['unlocked_skins']:
            self.data['selected_skin'] = skin_id
            self.save_data()
    
    def update_high_score(self, score):
        """Обновить рекорд"""
        if score > self.data['high_score']:
            self.data['high_score'] = score
            self.save_data()
    
    def get_coins(self):
        return self.data['coins']
    
    def get_high_score(self):
        return self.data['high_score']
    
    def is_skin_unlocked(self, skin_id):
        return skin_id in self.data['unlocked_skins']
    
    def get_selected_skin(self):
        return self.data['selected_skin']
