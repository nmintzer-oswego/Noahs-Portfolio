import json
from typing import List, Dict

class MenuItem:
    def __init__(self, name: str, price: float, ingredients: List[str], available: bool = True, in_stock: bool = True):
        self.name = name
        self.price = price
        self.ingredients = ingredients
        self.available = available
        self.in_stock = in_stock

    def model_dump(self) -> Dict:
        return {
            "name": self.name,
            "price": self.price,
            "ingredients": self.ingredients,
            "available": self.available,
            "in_stock": self.in_stock
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            name=data["name"],
            price=data["price"],
            ingredients=data["ingredients"],
            available=data["available"],
            in_stock=data["in_stock"]
        )

class MenuManager:
    def __init__(self):
        self.menu_items: List[MenuItem] = []

    def add_item(self, item: MenuItem):
        self.menu_items.append(item)
        print(f"Added {item.name} to the menu.")

    def edit_item(self, item_name: str, **kwargs):
        for item in self.menu_items:
            if item.name.lower() == item_name.lower():
                for key, value in kwargs.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                print(f"Updated {item.name} in the menu.")
                return
        print(f"Item '{item_name}' not found in the menu.")

    def remove_item(self, item_name: str):
        for item in self.menu_items:
            if item.name.lower() == item_name.lower():
                self.menu_items.remove(item)
                print(f"Removed {item.name} from the menu.")
                return
        print(f"Item '{item_name}' not found in the menu.")

    def display_menu(self):
        if not self.menu_items:
            print("The menu is empty.")
        else:
            print("\nCurrent Menu:")
            for item in self.menu_items:
                print(f"- {item.name}: ${item.price:.2f}")
                print(f"  Ingredients: {', '.join(item.ingredients)}")
                print(f"  Available: {'Yes' if item.available else 'No'}")
                print(f"  In Stock: {'Yes' if item.in_stock else 'No'}")
                print()

    def save_menu(self, filename: str):
        with open(filename, 'w') as f:
            json.dump([item.model_dump() for item in self.menu_items], f, indent=2)
        print(f"Menu saved to {filename}")

    def load_menu(self, filename: str):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.menu_items = [MenuItem.from_dict(item_data) for item_data in data]
            print(f"Menu loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty menu.")

def main():
    menu_manager = MenuManager()

    # Load existing menu if available
    menu_manager.load_menu("menu.json")

    while True:
        print("\nMenu Manager")
        print("1. Add item")
        print("2. Edit item")
        print("3. Remove item")
        print("4. Display menu")
        print("5. Save menu")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            ingredients = input("Enter ingredients (comma-separated): ").split(',')
            available = input("Is the item available? (y/n): ").lower() == 'y'
            in_stock = input("Is the item in stock? (y/n): ").lower() == 'y'
            menu_manager.add_item(MenuItem(name, price, ingredients, available, in_stock))

        elif choice == '2':
            name = input("Enter the name of the item to edit: ")
            print("Enter new values (press enter to keep current value):")
            new_name = input("New name: ")
            new_price = input("New price: ")
            new_ingredients = input("New ingredients (comma-separated): ")
            new_available = input("Is the item available? (y/n): ")
            new_in_stock = input("Is the item in stock? (y/n): ")

            kwargs = {}
            if new_name: kwargs['name'] = new_name
            if new_price: kwargs['price'] = float(new_price)
            if new_ingredients: kwargs['ingredients'] = new_ingredients.split(',')
            if new_available: kwargs['available'] = new_available.lower() == 'y'
            if new_in_stock: kwargs['in_stock'] = new_in_stock.lower() == 'y'

            menu_manager.edit_item(name, **kwargs)

        elif choice == '3':
            name = input("Enter the name of the item to remove: ")
            menu_manager.remove_item(name)

        elif choice == '4':
            menu_manager.display_menu()

        elif choice == '5':
            menu_manager.save_menu("menu.json")

        elif choice == '6':
            print("Exiting Menu Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
