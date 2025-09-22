from .db import Database
from .restaurant import RestaurantService

class NeatApp:
    def __init__(self, db_path=':memory:'):
        self.db = Database(db_path)
        self.restaurant_service = RestaurantService(self.db)

    def run(self):
        # Placeholder: Replace with actual application logic or web/CLI runner
        print('NeatApp is running!')

if __name__ == '__main__':
    app = NeatApp()
    app.run()