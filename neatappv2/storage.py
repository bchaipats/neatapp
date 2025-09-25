from neatapp.db import store_result, load_data_as_dataframe
import json

class StorageManager:
    def save_result(self, payload: dict, image_path: str):
        store_result(json.dumps(payload, indent=4), image_path)

    def load_all_data(self):
        return load_data_as_dataframe()