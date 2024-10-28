import unittest
from typing import List, Dict, Optional, Tuple, Union
from datetime import datetime, timedelta
import json
import os
import random
import importlib.util
import sys
from copy import deepcopy


def import_source_modules():
    """Import the source modules dynamically despite hyphens in filename"""
    current_dir = os.path.dirname(__file__)
    order_system_path = os.path.join(current_dir, "conversational-order-system.py")
    if not os.path.exists(order_system_path):
        raise FileNotFoundError(f"Could not find {order_system_path}")

    order_system_spec = importlib.util.spec_from_file_location("order_system", order_system_path)
    order_system = importlib.util.module_from_spec(order_system_spec)
    sys.modules[order_system_spec.name] = order_system  # This line is important
    order_system_spec.loader.exec_module(order_system)
    return order_system


# Import the required classes and functions
order_system = import_source_modules()
Menu = order_system.Menu
Order = order_system.Order
OrderProcessor = order_system.OrderProcessor
OrderTools = order_system.OrderTools
parse_takeout_order = order_system.parse_takeout_order


class ConversationLogger:
    """Helper class to log and display conversation details"""

    @staticmethod
    def format_order_summary(order: Order) -> str:
        """Format order details for display"""
        summary = []
        summary.append("\nOrder Summary:")
        summary.append(f"Customer: {order.customer_name}")
        summary.append(f"Phone: {order.phone_number}")
        summary.append("\nItems:")
        for item in order.order_items:
            item_str = f"- {OrderTools.get_item_name(item)} (Qty: {OrderTools.get_item_quantity(item)})"
            if hasattr(item, 'customizations') and item.customizations:
                item_str += f" - {item.customizations}"
            summary.append(item_str)
        summary.append(f"\nPickup Time: {order.pickup_time}")
        summary.append(f"Payment Method: {order.payment_method}")
        summary.append(f"Pickup Instructions: {order.pickup_instructions}")
        return "\n".join(summary)

    @staticmethod
    def format_conversation(conversation: List[str],
                            llm_responses: List[str],
                            expected_output: Dict,
                            actual_order: Optional[Order] = None,
                            test_result: Optional[str] = None) -> str:
        """Format the entire conversation and results for display"""
        output = ["\n" + "=" * 60]
        output.append("CONVERSATION FLOW:")
        output.append("=" * 60 + "\n")

        # Interleave customer messages and assistant responses
        for i, (customer_msg, assistant_msg) in enumerate(zip(conversation, llm_responses), 1):
            output.append(f"Customer {i}: {customer_msg}")
            output.append(f"Assistant: {assistant_msg}\n")

        output.append("=" * 60)
        output.append("EXPECTED OUTPUT:")
        output.append("=" * 60)
        output.append("Items:")
        for item in expected_output["order_items"]:
            output.append(f"- {item['item']} (Qty: {item['quantity']})")
        output.append(f"\nCustomer: {expected_output['customer_name']}")
        output.append(f"Phone: {expected_output['phone_number']}")
        output.append(f"Pickup Time: {expected_output['pickup_time']}")

        if actual_order:
            output.append("\n" + "=" * 60)
            output.append("ACTUAL OUTPUT:")
            output.append("=" * 60)
            output.append(ConversationLogger.format_order_summary(actual_order))

        if test_result:
            output.append("\n" + "=" * 60)
            output.append("TEST RESULT:")
            output.append("=" * 60)
            output.append(test_result)

        output.append("=" * 60 + "\n")
        return "\n".join(output)


class ConversationalTestData:
    def __init__(self):
        self.greetings = [
            "Hi, I'd like to place an order",
            "Hello, I'm calling to order some food",
            "Good evening, I want to order takeout",
            "Hey there, I'd like to order something",
        ]
        self.menu_questions = [
            "Can you tell me what's in the Margherita Pizza?",
            "What vegetables come in the Vegetarian Pasta?",
            "Is the Caesar Salad big enough for sharing?",
            "How spicy is the Vegetarian Pasta?"
        ]
        self.ordering_phrases = [
            "I would like to order",
            "I'll have",
            "Let me get",
            "I want to order",
            "Please add"
        ]
        self.natural_time_phrases = [
            "I'll pick it up at",
            "Can I get that for",
            "Is it possible to pick up at",
            "Would pickup at",
            "Planning to come by at"
        ]

    def generate_natural_conversation(self, menu_items: List[Dict]) -> Tuple[List[str], Dict]:
        """Generate a natural conversation flow for ordering"""
        conversation = []
        expected_output = {
            "order_items": [],
            "payment_method": "Pay upon pickup",
            "pickup_instructions": "In-store pickup"
        }

        # Start with greeting
        conversation.append(random.choice(self.greetings))

        # Optional menu question (50% chance)
        if random.random() < 0.5:
            conversation.append(random.choice(self.menu_questions))

        # Place the main order
        main_item = random.choice(menu_items)
        order_phrase = random.choice(self.ordering_phrases)
        conversation.append(f"{order_phrase} a {main_item['name']}")
        expected_output["order_items"].append({
            "item": main_item['name'],
            "quantity": 1
        })

        # Add customer information
        name = f"{random.choice(['John', 'Jane', 'Bob', 'Alice', 'Charlie'])} {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Davis'])}"
        phone = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        conversation.append(f"My name is {name} and my number is {phone}")
        expected_output["customer_name"] = name
        expected_output["phone_number"] = phone

        # Add pickup time
        hour = random.randint(1, 12)
        minute = random.choice(['00', '15', '30', '45'])
        period = random.choice(['AM', 'PM'])
        pickup_time = f"{hour}:{minute} {period}"
        time_phrase = random.choice(self.natural_time_phrases)
        conversation.append(f"{time_phrase} {pickup_time}")
        expected_output["pickup_time"] = pickup_time

        return conversation, expected_output


class ConversationalOrderSystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.menu = Menu("menu.json")
        cls.order_processor = OrderProcessor(cls.menu)
        cls.test_data = ConversationalTestData()
        cls.logger = ConversationLogger()

        # Load menu items
        with open("menu.json", 'r') as f:
            cls.menu_items = [item for item in json.load(f) if item['available'] and item['in_stock']]

    def setUp(self):
        os.makedirs("../Orders", exist_ok=True)

    def tearDown(self):
        for filename in os.listdir("../Orders"):
            if filename.startswith("order_"):
                os.remove(os.path.join("../Orders", filename))

    def test_basic_order(self):
        """Test a basic order flow"""
        conversation = [
            "Hi, I'd like to place an order",
            "I'll have a Margherita Pizza",
            "My name is John Smith and my number is 123-456-7890",
            "I'll pick it up at 6:30 PM"
        ]
        
        expected_output = {
            "customer_name": "John Smith",
            "phone_number": "123-456-7890",
            "pickup_time": "6:30 PM",
            "order_items": [
                {"item": "Margherita Pizza", "quantity": 1}
            ],
            "payment_method": "Pay upon pickup",
            "pickup_instructions": "In-store pickup"
        }
        
        result = self.process_test_order(conversation)
        self.assertIsNotNone(result)
        self.verify_order(result, expected_output, conversation)

    def process_test_order(self, conversation: List[str]) -> Tuple[Optional[Order], List[str]]:
        """Process a test order and return the resulting Order object and responses"""
        current_order = Order()
        formatted_conversation = []
        llm_responses = []

        for msg in conversation:
            formatted_conversation.append(f"Customer: {msg}")

            # Get LLM response for this message
            parsed_order, missing_info = parse_takeout_order(self.menu, formatted_conversation)

            if parsed_order:
                current_order, should_continue, error_message = self.order_processor.handle_parsed_order(
                    parsed_order, current_order, None, False
                )

                # Generate appropriate response based on the current state
                if error_message:
                    response = f"I apologize, but {error_message}"
                else:
                    response = self.generate_response(parsed_order, current_order, missing_info)
                llm_responses.append(response)
            else:
                if missing_info:
                    response = f"I still need some information: {missing_info}"
                else:
                    response = "I'm sorry, I'm having trouble understanding. Could you please clarify?"
                llm_responses.append(response)

        return current_order, llm_responses

    def verify_order(self, result: Order, expected_output: Dict, conversation: List[str]):
        """Verify that the order matches the expected output"""
        try:
            result_dict = result.model_dump()

            # Print conversation and results for debugging
            print("\nTEST CONVERSATION:")
            for i, msg in enumerate(conversation, 1):
                print(f"{i}. Customer: {msg}")

            print("EXPECTED OUTPUT:")
            print(json.dumps(expected_output, indent=2))

            print("ACTUAL OUTPUT:")
            print(json.dumps(result_dict, indent=2))

            # Verify basic fields
            self.assertEqual(result_dict["customer_name"], expected_output["customer_name"])
            self.assertEqual(result_dict["phone_number"], expected_output["phone_number"])
            self.assertEqual(result_dict["pickup_time"], expected_output["pickup_time"])

            # Sort and normalize order items for comparison
            expected_items = sorted(
                expected_output["order_items"],
                key=lambda x: (x["item"], x.get("quantity", 1))
            )
            result_items = sorted(
                [{"item": OrderTools.get_item_name(item),  # Changed from self.OrderTools to OrderTools
                  "quantity": OrderTools.get_item_quantity(item)}  # Changed here too
                 for item in result.order_items],
                key=lambda x: (x["item"], x["quantity"])
            )

            # Compare items
            self.assertEqual(len(result_items), len(expected_items),
                             f"Expected {len(expected_items)} items, got {len(result_items)}")
            for exp_item, res_item in zip(expected_items, result_items):
                self.assertEqual(exp_item["item"], res_item["item"])
                self.assertEqual(exp_item["quantity"], res_item["quantity"])

            # Log successful test
            print(self.logger.format_conversation(
                conversation,
                expected_output,
                result,
                "✓ Test passed successfully"
            ))

        except AssertionError as e:
            # Log failed test with details
            print(self.logger.format_conversation(
                conversation,
                expected_output,
                result,
                f"✗ Test failed: {str(e)}"
            ))
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
