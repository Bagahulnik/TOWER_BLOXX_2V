"""Управление сохранением прогресса и настроек"""
import json
import os
from config import TOWER_SKINS, DEFAULT_SETTINGS


class SaveManager:
    def __init__(self, save_file="save_data.json"):
        self.save_file = save_file
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    if "settings" not in data:
                        data["settings"] = DEFAULT_SETTINGS.copy()

                    # КОНВЕРТАЦИЯ ЧИСЕЛ В СТРОКИ 'tower_X'
                    if isinstance(data.get("selected_skin"), int):
                        data["selected_skin"] = f"tower_{data['selected_skin']}"
                    if "unlocked_skins" in data:
                        new_list = []
                        for s in data["unlocked_skins"]:
                            if isinstance(s, int):
                                new_list.append(f"tower_{s}")
                            else:
                                new_list.append(s)
                        data["unlocked_skins"] = new_list

                    return data
            except:
                pass

        return {
            "coins": 0,
            "high_score": 0,
            "unlocked_skins": ["tower_1"],
            "selected_skin": "tower_1",
            "settings": DEFAULT_SETTINGS.copy(),
        }

    def save_data(self):
        try:
            with open(self.save_file, "w") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    def get_coins(self):
        return self.data.get("coins", 0)

    def add_coins(self, amount):
        self.data["coins"] = self.get_coins() + amount
        self.save_data()

    def spend_coins(self, amount):
        if self.get_coins() >= amount:
            self.data["coins"] = self.get_coins() - amount
            self.save_data()
            return True
        return False

    def get_high_score(self):
        return self.data.get("high_score", 0)

    def update_high_score(self, score):
        if score > self.get_high_score():
            self.data["high_score"] = score
            self.save_data()

    def is_skin_unlocked(self, skin_id):
        return skin_id in self.data.get("unlocked_skins", [])

    def unlock_skin(self, skin_id):
        if skin_id not in self.data["unlocked_skins"]:
            self.data["unlocked_skins"].append(skin_id)
            self.save_data()

    def get_selected_skin(self):
        return self.data.get("selected_skin", "tower_1")

    def set_selected_skin(self, skin_id):
        self.data["selected_skin"] = skin_id
        self.save_data()

    # настройки — как было
    def get_settings(self):
        if "settings" not in self.data:
            self.data["settings"] = DEFAULT_SETTINGS.copy()
        return self.data["settings"]

    def get_music_volume(self):
        return self.get_settings().get("music_volume", 0.5)

    def set_music_volume(self, volume):
        self.data["settings"]["music_volume"] = max(0.0, min(1.0, volume))
        self.save_data()

    def get_sound_volume(self):
        return self.get_settings().get("sound_volume", 0.7)

    def set_sound_volume(self, volume):
        self.data["settings"]["sound_volume"] = max(0.0, min(1.0, volume))
        self.save_data()

    def get_selected_background(self):
        return self.get_settings().get("selected_background", 0)

    def set_selected_background(self, bg_index):
        self.data["settings"]["selected_background"] = bg_index
        self.save_data()
