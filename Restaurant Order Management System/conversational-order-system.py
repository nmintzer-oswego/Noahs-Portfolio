import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from typing import List, Dict, Optional, Set, Tuple
from pydantic import BaseModel
from copy import deepcopy
import logging
import logging.handlers
import os
from datetime import datetime, timedelta
from simple_response_config import ResponseTemplates

os.environ[
    "OPENAI_API_KEY"] = "OPENAI API KEY"


# Menu Item and Menu classes (updated)
class MenuItem(BaseModel):
    name: str
    price: float
    ingredients: List[str]
    available: bool
    in_stock: bool


class Menu:
    def __init__(self, filename: str):
        self.items: List[MenuItem] = []
        self.load_menu(filename)

    def load_menu(self, filename: str):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.items = [MenuItem(**item) for item in data]
            print(f"Menu loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found. Please ensure the menu file exists.")

    def display_menu(self):
        if not self.items:
            print("The menu is empty.")
        else:
            print("\nCurrent Menu:")
            for item in self.items:
                if item.available and item.in_stock:
                    print(f"- {item.name}: ${item.price:.2f}")
                    print(f"  Ingredients: {', '.join(item.ingredients)}")
                    print()

    def get_item_price(self, item_name: str) -> Optional[float]:
        for item in self.items:
            if item.name.lower() == item_name.lower() and item.available and item.in_stock:
                return item.price
        return None

    def is_item_on_menu(self, item_name: str) -> bool:
        return any(item.name.lower() == item_name.lower() for item in self.items)


# Updated Order classes
class OrderItem(BaseModel):
    item: str = Field(description="The name of the menu item")
    quantity: int = Field(description="The quantity of this item ordered")
    customizations: Optional[str] = Field(default=None,
                                          description="Any customizations or special requests for this item")


class Order(BaseModel):
    customer_name: Optional[str] = Field(default=None, description="The customer's full name")
    phone_number: Optional[str] = Field(default=None, description="The customer's phone number")
    order_items: Optional[List[Union[OrderItem, Dict]]] = Field(default=None, description="List of items ordered")
    pickup_time: Optional[str] = Field(default=None, description="The desired pickup time")
    payment_method: Optional[str] = Field(default="Pay upon pickup",
                                          description="Whether the customer will pay upon pickup or over the phone")
    dietary_restrictions: Optional[str] = Field(default=None, description="Any dietary restrictions or allergies")
    pickup_instructions: Optional[str] = Field(default="In-store pickup",
                                               description="Whether it's curbside, in-store, or through a delivery service")


# Initialize the LLM
llm = OpenAI(temperature=0)

# Create a parser
parser = PydanticOutputParser(pydantic_object=Order)

# Create a prompt template
template = """
You are an AI assistant helping customers place takeout orders for a restaurant. 
Extract the following information from the customer's order conversation:

{format_instructions}

Current Menu:
{menu_items}

Customer order conversation:
{order_conversation}

Make sure to include payment_method and pickup_instructions in your response when the customer finishes their order, even if they are not explicitly mentioned by the customer. Use default values if necessary.
If any required information is missing, respond with INCOMPLETE_ORDER and list the missing fields.

Extracted order information:"""


prompt = PromptTemplate(
    template=template,
    input_variables=["menu_items", "order_conversation"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)


# Configure logging
def setup_logger() -> logging.Logger:
    """
    Configure and return a logger with both file and console handlers.
    The file handler rotates logs daily and keeps 30 days of history.
    """
    # Create logs directory if it doesn't exist
    log_dir = "../logs"
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger("OrderSystem")
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times
    if not logger.handlers:
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )

        # Create and configure file handler (rotating daily)
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_dir, 'order_system.log'),
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)

        # Create and configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Only show warnings and errors in console
        console_handler.setFormatter(console_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Create logger instance
logger = setup_logger()


# Add a function to log exceptions with full traceback
def log_exception(e: Exception, message: str = "An error occurred"):
    """
    Log an exception with full traceback information.

    Args:
        e: The exception that was caught
        message: Optional message to precede the error
    """
    import traceback
    logger.error(
        f"{message}: {str(e)}\nTraceback:\n{''.join(traceback.format_tb(e.__traceback__))}"
    )


# Update the OrderProcessor class to use the logger
class OrderProcessor:
    def __init__(self, menu: Menu):
        self.menu = menu
        self.order_tools = OrderTools()
        self.MAX_QUANTITY = 100
        self.response_generator = ResponseGenerator()
        self.logger = logging.getLogger("OrderSystem")  # Get logger instance

    def take_order(self) -> None:
        """Main function to handle the order-taking process with error handling."""
        try:
            conversation, current_order, last_valid_order, modification_mode = (
                self.initialize_order()
            )
            self.logger.info("New order session initialized")

            while True:
                try:
                    user_input = input("Customer: ").strip()
                    if not user_input:
                        print("Please provide your order details.")
                        continue

                    if user_input.lower() == "done":
                        self.logger.info("Order session completed")
                        break

                    self.logger.info(f"Received user input: {user_input}")

                    # Rest of the take_order method implementation...
                    # Replace existing logger calls with self.logger calls

                except Exception as e:
                    log_exception(e, "Error processing user input")
                    print("I apologize, but there was an error processing your input. "
                          "Please try again.")
                    continue

        except Exception as e:
            log_exception(e, "Fatal error in take_order")
            print("I apologize, but there was a system error. Please try again later.")
class OrderSystemException(Exception):
    """Base exception class for the order system"""
    pass

class MenuError(OrderSystemException):
    """Raised for menu-related errors"""
    pass

class OrderValidationError(OrderSystemException):
    """Raised when order validation fails"""
    pass

class OrderProcessingError(OrderSystemException):
    """Raised when order processing fails"""
    pass

class LLMError(OrderSystemException):
    """Raised when there's an error with the LLM processing"""
    pass


def parse_takeout_order(menu: Menu, order_conversation: List[str]) -> Tuple[Optional[Order], Optional[str]]:
    """
    Parse order from conversation history with comprehensive error handling.

    Args:
        menu: Menu instance containing available items
        order_conversation: List of conversation messages

    Returns:
        Tuple of (parsed_order, error_message)

    Raises:
        MenuError: If there's an issue with the menu
        LLMError: If there's an issue with the LLM processing
        OrderValidationError: If there's an issue with order validation
    """
    logger.info("Starting order parsing")
    try:
        # Validate menu has items
        if not menu.items:
            logger.error("Attempted to parse order with empty menu")
            raise MenuError("Menu is empty")

        # Get available menu items
        try:
            menu_items = "\n".join(
                [f"{item.name}: ${item.price:.2f}"
                 for item in menu.items
                 if item.available and item.in_stock]
            )
            if not menu_items:
                logger.error("No available items found in menu")
                raise MenuError("No items are currently available")
            logger.debug(f"Available menu items: {menu_items}")
        except Exception as e:
            log_exception(e, "Error processing menu items")
            raise MenuError(f"Error processing menu items: {str(e)}")

        # Process conversation
        try:
            conversation_text = "\n".join(order_conversation)
            logger.debug(f"Processing conversation: {conversation_text}")
        except Exception as e:
            log_exception(e, "Error processing conversation")
            raise OrderValidationError(f"Error processing conversation: {str(e)}")

        # Make LLM call with timeout and retry logic
        try:
            logger.debug("Making LLM API call")
            llm_response = llm.invoke(
                prompt.format(
                    menu_items=menu_items,
                    order_conversation=conversation_text
                ),
                timeout=10  # 10 second timeout
            )
            logger.debug(f"LLM response received: {llm_response}")
        except Exception as e:
            log_exception(e, "Error in LLM API call")
            raise LLMError(f"Error getting response from LLM: {str(e)}")

        # Handle incomplete orders
        if "INCOMPLETE_ORDER" in llm_response:
            missing_info = llm_response.split("INCOMPLETE_ORDER")[1].strip()
            logger.info(f"Incomplete order detected: {missing_info}")
            return None, f"Missing information: {missing_info}"

        # Parse the response
        try:
            parsed_order = parser.parse(llm_response)
            logger.debug(f"Successfully parsed order: {parsed_order}")
        except Exception as e:
            log_exception(e, "Error parsing LLM response")
            raise OrderValidationError(f"Error parsing order: {str(e)}")

        # Validate parsed order
        if not parsed_order:
            logger.error("Parser returned None for order")
            raise OrderValidationError("Failed to parse order")

        logger.info("Successfully completed order parsing")
        return parsed_order, None

    except MenuError as e:
        log_exception(e, "Menu error")
        return None, f"Menu system error: {str(e)}"
    except LLMError as e:
        log_exception(e, "LLM error")
        return None, "Sorry, I'm having trouble processing your order right now. Please try again."
    except OrderValidationError as e:
        log_exception(e, "Order validation error")
        return None, f"Order validation error: {str(e)}"
    except Exception as e:
        log_exception(e, "Unexpected error in parse_takeout_order")
        return None, "An unexpected error occurred. Please try again."

def calculate_total(menu: Menu, order: Order) -> float:
    total = 0
    if order.order_items:
        for item in order.order_items:
            if isinstance(item, dict):
                item_name = item.get('item', '')
                quantity = item.get('quantity', 1)
            else:
                item_name = item.item
                quantity = item.quantity
            price = menu.get_item_price(item_name)
            if price is not None:
                total += price * quantity
    return total


class OrderTools:
    @staticmethod
    def get_item_name(item: Union[OrderItem, Dict]) -> str:
        """
        Safely get item name regardless of type.

        Args:
            item: Either OrderItem object or dictionary

        Returns:
            Item name as string
        """
        return item.item if isinstance(item, OrderItem) else item['item']

    @staticmethod
    def get_item_quantity(item: Union[OrderItem, Dict]) -> int:
        """
        Safely get item quantity regardless of type.

        Args:
            item: Either OrderItem object or dictionary

        Returns:
            Item quantity as integer
        """
        return item.quantity if isinstance(item, OrderItem) else item['quantity']

    @staticmethod
    def create_order_item(item: Union[OrderItem, Dict]) -> OrderItem:
        """
        Create an OrderItem from either an OrderItem or dictionary.

        Args:
            item: Either OrderItem object or dictionary

        Returns:
            OrderItem object
        """
        if isinstance(item, OrderItem):
            return deepcopy(item)
        return OrderItem(
            item=item['item'],
            quantity=item['quantity'],
            customizations=item.get('customizations')
        )

    @staticmethod
    def merge_items(current_items: List[Union[OrderItem, Dict]],
                    new_items: List[Union[OrderItem, Dict]],
                    replace_quantities: bool = False) -> List[OrderItem]:
        """
        Merge two lists of items, handling both OrderItem and dict types.

        Args:
            current_items: Current list of items
            new_items: New items to merge
            replace_quantities: If True, replace quantities; if False, add them

        Returns:
            List of merged OrderItems
        """
        # Convert current items to OrderItem objects if they aren't already
        result = [OrderTools.create_order_item(item) for item in current_items] if current_items else []

        for new_item in new_items:
            new_item_name = OrderTools.get_item_name(new_item)
            new_item_quantity = OrderTools.get_item_quantity(new_item)

            # Find matching item in result
            existing_item = next(
                (item for item in result
                 if OrderTools.get_item_name(item).lower() == new_item_name.lower()),
                None
            )

            if existing_item:
                if replace_quantities:
                    existing_item.quantity = new_item_quantity
                else:
                    existing_item.quantity += new_item_quantity
            else:
                result.append(OrderTools.create_order_item(new_item))

        return result

from response_generator import ResponseGenerator

class OrderProcessor:
    def __init__(self, menu: Menu):
        self.menu = menu
        self.order_tools = OrderTools()
        self.MAX_QUANTITY = 100
        self.response_generator = ResponseGenerator()


    def initialize_order(self) -> Tuple[List[str], Order, Order, bool]:
        """Initialize a new order session."""
        print(f"\n{ResponseTemplates.get_response('WELCOME')}")
        return [], Order(), None, False

    def validate_quantities(self, order_items: List[Union[OrderItem, Dict]]) -> Tuple[bool, List[str]]:
        """
        Validate quantities for all items in the order.
        Returns (is_valid, list of invalid items)
        """
        invalid_quantities = []
        for item in order_items:
            quantity = self.order_tools.get_item_quantity(item)
            if not (0 < quantity <= self.MAX_QUANTITY):
                invalid_quantities.append(
                    f"{self.order_tools.get_item_name(item)} (Quantity: {quantity})"
                )
        return len(invalid_quantities) == 0, invalid_quantities

    def validate_menu_items(self, order_items: List[Union[OrderItem, Dict]]) -> Tuple[bool, List[str]]:
        """
        Validate all items against the menu.
        Returns (is_valid, list of invalid items)
        """
        off_menu_items = []
        for item in order_items:
            item_name = self.order_tools.get_item_name(item)
            if not self.menu.is_item_on_menu(item_name):
                off_menu_items.append(item_name)
        return len(off_menu_items) == 0, off_menu_items

    def validate_order_completeness(self, order: Order) -> Tuple[bool, List[str]]:
        """
        Check if all required fields are present.
        Returns (is_valid, list of missing fields)
        """
        missing_fields = []
        if not order.customer_name:
            missing_fields.append("name")
        if not order.phone_number:
            missing_fields.append("phone number")
        if not order.order_items:
            missing_fields.append("order items")
        if not order.pickup_time:
            missing_fields.append("pickup time")
        return len(missing_fields) == 0, missing_fields

    def process_modification(self, current_order: Order, parsed_order: Order,
                             last_valid_order: Optional[Order]) -> Order:
        """Process order modification and return updated order."""
        working_order = deepcopy(last_valid_order) if last_valid_order else current_order
        working_order.order_items = self.order_tools.merge_items(
            working_order.order_items or [],
            parsed_order.order_items,
            replace_quantities=False
        )
        return working_order

    def update_order_info(self, current_order: Order, parsed_order: Order) -> None:
        """Update non-item order information."""
        preserved_fields = {'payment_method', 'pickup_instructions'} if current_order.payment_method else set()
        for field, value in parsed_order.model_dump().items():
            if value is not None and field != 'order_items' and field not in preserved_fields:
                setattr(current_order, field, value)

    def display_order_summary(self, order: Order, total: float) -> None:
        """Display the current order summary."""
        order_items = ", ".join([
            f"{self.order_tools.get_item_name(item)} (Quantity: {self.order_tools.get_item_quantity(item)})"
            + (f" with {item.customizations}" if getattr(item, 'customizations', None) else "")
            for item in order.order_items
        ])

        print(ResponseTemplates.get_response(
            'ORDER_SUMMARY',
            customer_name=order.customer_name,
            order_items=order_items,
            total=f"${total:.2f}",
            pickup_time=order.pickup_time
        ))

    def handle_parsed_order(self,
                            parsed_order: Order,
                            current_order: Order,
                            last_valid_order: Optional[Order],
                            modification_mode: bool) -> Tuple[Order, bool, Optional[str]]:
        """Handle a successfully parsed order."""
        context = {
            "customer_name": current_order.customer_name,
            "is_modification": modification_mode,
            "current_items": str(current_order.order_items) if current_order.order_items else None
        }

        # Validate quantities
        quantities_valid, invalid_quantities = self.validate_quantities(parsed_order.order_items)
        if not quantities_valid:
            print(ResponseTemplates.get_response(
                'INVALID_ITEMS',
                invalid_items=", ".join(invalid_quantities)
            ))
            return current_order, True, f"Invalid quantities for: {', '.join(invalid_quantities)}"

        # Update order based on mode
        if modification_mode and parsed_order.order_items:
            current_order = self.process_modification(current_order, parsed_order, last_valid_order)
        elif parsed_order.order_items:
            current_order.order_items = self.order_tools.merge_items(
                current_order.order_items or [],
                parsed_order.order_items,
                replace_quantities=False
            )

        # Update other information
        self.update_order_info(current_order, parsed_order)

        # Validate menu items
        menu_valid, off_menu_items = self.validate_menu_items(current_order.order_items or [])
        if not menu_valid:
            response = self.response_generator.generate_response(
                context={**context, "invalid_items": off_menu_items},
                response_type="INVALID_MENU_ITEMS",
                notes="Items ordered are not on the menu"
            )
            print(response)
            return current_order, True, f"Items not on menu: {', '.join(off_menu_items)}"

        # Validate completeness
        complete, missing_fields = self.validate_order_completeness(current_order)
        if not complete:
            response = self.response_generator.generate_response(
                context={**context, "missing_fields": missing_fields},
                response_type="MISSING_INFORMATION",
                notes="Order is missing required information"
            )
            print(response)
            return current_order, True, f"Missing information: {', '.join(missing_fields)}"

        return current_order, False, None

    def handle_parsed_order(
            self,
            parsed_order: Order,
            current_order: Order,
            last_valid_order: Optional[Order],
            modification_mode: bool
    ) -> Tuple[Order, bool, Optional[str]]:
        """
        Handle a parsed order with comprehensive error handling.

        Returns:
            Tuple of (updated_order, should_continue, error_message)
        """
        try:
            # Validate parsed order exists
            if not parsed_order:
                raise OrderValidationError("No order data provided")

            # Validate quantities
            if parsed_order.order_items:
                quantities_valid, invalid_quantities = self.validate_quantities(
                    parsed_order.order_items
                )
                if not quantities_valid:
                    raise OrderValidationError(
                        f"Invalid quantities for: {', '.join(invalid_quantities)}"
                    )

            # Handle order modification
            try:
                if modification_mode and parsed_order.order_items:
                    current_order = self.process_modification(
                        current_order, parsed_order, last_valid_order
                    )
                elif parsed_order.order_items:
                    current_order.order_items = self.order_tools.merge_items(
                        current_order.order_items or [],
                        parsed_order.order_items,
                        replace_quantities=False
                    )
            except Exception as e:
                raise OrderProcessingError(f"Error modifying order: {str(e)}")

            # Update order information
            try:
                self.update_order_info(current_order, parsed_order)
            except Exception as e:
                raise OrderProcessingError(f"Error updating order info: {str(e)}")

            # Validate menu items
            menu_valid, off_menu_items = self.validate_menu_items(
                current_order.order_items or []
            )
            if not menu_valid:
                raise OrderValidationError(
                    f"Items not on menu: {', '.join(off_menu_items)}"
                )

            # Validate order completeness
            complete, missing_fields = self.validate_order_completeness(current_order)
            if not complete:
                raise OrderValidationError(
                    f"Missing information: {', '.join(missing_fields)}"
                )

            return current_order, False, None

        except OrderValidationError as e:
            logger.error(f"Order validation error: {str(e)}")
            return current_order, True, str(e)
        except OrderProcessingError as e:
            logger.error(f"Order processing error: {str(e)}")
            return current_order, True, str(e)
        except Exception as e:
            logger.error(f"Unexpected error in handle_parsed_order: {str(e)}")
            return current_order, True, "An unexpected error occurred. Please try again."

    def take_order(self) -> None:
        """Main function to handle the order-taking process with error handling."""
        try:
            conversation, current_order, last_valid_order, modification_mode = (
                self.initialize_order()
            )

            while True:
                try:
                    user_input = input("Customer: ").strip()
                    if not user_input:
                        print("Please provide your order details.")
                        continue

                    if user_input.lower() == "done":
                        break

                    # Update conversation based on mode
                    if modification_mode:
                        conversation = [f"Customer: {user_input}"]
                    else:
                        conversation.append(f"Customer: {user_input}")

                    # Parse the order
                    parsed_order, missing_info = parse_takeout_order(
                        self.menu, conversation
                    )

                    if parsed_order:
                        current_order, should_continue, error_message = (
                            self.handle_parsed_order(
                                parsed_order,
                                current_order,
                                last_valid_order,
                                modification_mode
                            )
                        )

                        if error_message:
                            print(f"I apologize, but {error_message}")
                            if "not on menu" in error_message:
                                print("Would you like to see our menu or order something else?")
                            print("Please try again.")
                            continue

                        # Calculate total and display summary
                        try:
                            total = calculate_total(self.menu, current_order)
                            self.display_order_summary(current_order, total)
                        except Exception as e:
                            logger.error(f"Error displaying order summary: {str(e)}")
                            print("I apologize, but I'm having trouble displaying your order. "
                                  "Let me start over.")
                            continue

                        # Handle order confirmation
                        confirm = input("\nIs this correct? (yes/no): ").lower()
                        if confirm == 'yes':
                            try:
                                save_order_to_file(current_order, total)
                                print("Thank you for your order!")
                                return
                            except Exception as e:
                                logger.error(f"Error saving order: {str(e)}")
                                print("I apologize, but there was an error saving your order. "
                                      "Please try again.")
                                continue
                        elif confirm == 'no':
                            print("I apologize for any mistakes. Please let me know what needs "
                                  "to be changed.")
                            last_valid_order = deepcopy(current_order)
                            modification_mode = True
                            continue
                        else:
                            print("Please answer 'yes' or 'no'.")
                            continue

                    elif missing_info:
                        print(f"I still need some information to complete your order: "
                              f"{missing_info}")
                        print("Please provide the missing details or any other information "
                              "you'd like to add.")
                    else:
                        print("I'm having trouble understanding your order. Could you please "
                              "provide more details?")

                except Exception as e:
                    logger.error(f"Error processing user input: {str(e)}")
                    print("I apologize, but there was an error processing your input. "
                          "Please try again.")
                    continue

        except Exception as e:
            logger.error(f"Fatal error in take_order: {str(e)}")
            print("I apologize, but there was a system error. Please try again later.")

    def _format_order_items(self, order_items: List[Union[OrderItem, Dict]]) -> str:
        """Format order items for display in responses"""
        formatted_items = []
        for item in order_items:
            item_name = self.order_tools.get_item_name(item)
            quantity = self.order_tools.get_item_quantity(item)
            customizations = (
                item.customizations if isinstance(item, OrderItem)
                else item.get('customizations')
            )

            item_str = f"{quantity} {item_name}"
            if customizations:
                item_str += f" ({customizations})"
            formatted_items.append(item_str)

        return ", ".join(formatted_items)


def validate_quantity(quantity: int) -> bool:
    """
    Validate if the order quantity is reasonable.

    Args:
        quantity: The quantity to validate

    Returns:
        bool: True if quantity is valid, False otherwise
    """
    MAX_QUANTITY = 100  # Maximum reasonable quantity for any item
    return 0 < quantity <= MAX_QUANTITY


def save_order_to_file(order: Order, total: float):
    """
    Save the order to a JSON file in the Orders directory.
    Creates the Orders directory if it doesn't exist.
    """
    # Create Orders directory if it doesn't exist
    orders_dir = "../Orders"
    os.makedirs(orders_dir, exist_ok=True)

    # Prepare the order data
    order_dict = order.model_dump()
    order_dict['total'] = total
    order_dict['timestamp'] = datetime.now().isoformat()

    # Convert all items to dictionaries for JSON serialization
    if order_dict['order_items']:
        order_dict['order_items'] = [
            {
                'item': OrderTools.get_item_name(item),
                'quantity': OrderTools.get_item_quantity(item),
                'customizations': (item.customizations if isinstance(item, OrderItem)
                                   else item.get('customizations'))
            }
            for item in order_dict['order_items']
        ]

    # Create filename with path
    filename = f"order_{order.customer_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(orders_dir, filename)

    # Save the file
    with open(filepath, 'w') as f:
        json.dump(order_dict, f, indent=2)

    print(f"Order saved to {filepath}")


def main():
    menu = Menu("menu.json")

    while True:
        print("\nWelcome to our restaurant!")
        print("1. View Menu")
        print("2. Place Order")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            menu.display_menu()
        elif choice == '2':
            order_processor = OrderProcessor(menu)
            order_processor.take_order()
        elif choice == '3':
            print("Thank you for using our service. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
