# Restaurant Order Management System

A comprehensive Python-based system for managing restaurant orders with a conversational interface, menu management, and order processing capabilities.

## 🌟 Features

### Menu Management
- JSON-based menu storage system
- Add, edit, and remove menu items
- Track item availability and stock status
- Store item details including prices, ingredients, and customization options

### Order Processing
- Conversational interface for taking orders
- Real-time order validation
- Support for:
  - Multiple items per order
  - Special instructions and customizations
  - Dietary restrictions
  - Various pickup options (in-store, curbside)
  - Different payment methods
- Order modification capabilities
- Automatic total calculation

### Data Management
- Secure order storage in JSON format
- Organized order history
- Comprehensive customer information tracking
- Timestamp-based order tracking

## 🛠️ Technical Architecture

### Core Components
1. **Menu System** (`restaurant-menu-manager.py`)
   - MenuItem class for item representation
   - MenuManager class for menu operations
   - JSON-based persistence

2. **Order System** (`conversational-order-system.py`)
   - OrderItem and Order classes
   - OrderProcessor for handling orders
   - Natural language processing for order interpretation
   - Real-time validation and error handling

3. **Testing Framework** (`order-system-test.py`)
   - Comprehensive test cases
   - Order validation testing
   - Menu operation testing

4. **Error Handling & Logging**
   - Detailed error tracking
   - Comprehensive logging system
   - Validation at multiple levels

## 📋 Prerequisites

- Python 3.8+
- Required Python packages:
  ```
  pydantic
  langchain_openai
  ```

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nmintzer-oswego/Noahs-Portfolio.git
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the menu:
   ```bash
   python restaurant-menu-manager.py
   ```

## 💻 Usage

### Starting the System
```bash
python conversational-order-system.py
```

### Menu Management
```bash
python restaurant-menu-manager.py
```

### Running Tests
```bash
python order-system-test.py
```

## 📝 Example Order Flow

1. View the menu:
   ```
   Welcome to our restaurant!
   1. View Menu
   2. Place Order
   3. Exit
   ```

2. Place an order:
   ```
   Customer: I'd like to order a Margherita Pizza
   System: Could you please provide your name and phone number?
   Customer: My name is John Doe, phone is 123-456-7890
   System: What time would you like to pick up your order?
   ```
   3. Order verification:
   ```
    Welcome! I'll be happy to take your order. Please provide your name, phone number, and what you'd like to order.
    Customer: This is Alice, my number is 444-555-6666. I have a gluten allergy. Can I get the Grilled Chicken Salad without croutons? And a Lemonade please. I'll pick up at 7:15 PM.
    Great! Let me confirm your order Alice. You've ordered: Grilled Chicken Salad (Quantity: 1) with No croutons, Lemonade (Quantity: 1). The total is $11.99 for pickup at 7:15 PM.
    Is this correct? (yes/no): yes
    Order saved to ../Orders\order_Alice_20241028_181311.json
    Thank you for your order!
   ```
## 🏗️ Project Structure

```
.
├── conversational-order-system.py  # Main order processing system
├── restaurant-menu-manager.py      # Menu management system
├── order-system-test.py           # Testing framework
├── menu.json                      # Menu data
└── Orders/                        # Order storage directory
```

## 🔍 Error Handling

The system includes comprehensive error handling for:
- Invalid menu items
- Unreasonable quantities
- Missing customer information
- File operation errors
- Data validation issues

## 📊 Logging

Detailed logging is implemented for:
- Order processing steps
- Menu operations
- Error tracking
- System operations

## 🔐 Security Considerations

- Customer data is stored locally
- Payment information is not stored
- Access to order history is controlled


## 📄 License

[Apache License 2.0]

## 👥 Authors

[Noah Mintzer: https://www.linkedin.com/in/noah-mintzer-733404271/]

## 🙏 Acknowledgments

- Built with Python and Pydantic
- Uses LangChain for natural language processing
- JSON for data storage
