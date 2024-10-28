class ResponseTemplates:
    # Static responses for different situations
    RESPONSES = {
        "WELCOME": "Welcome! I'll be happy to take your order. Please provide your name, phone number, and what you'd like to order.",
        
        "MISSING_INFO": "I still need some information to complete your order: {missing_info}. Please provide the missing details.",
        
        "INVALID_ITEMS": "I apologize, but {invalid_items} are not available on our menu. Would you like to see our menu or order something else?",
        
        "ORDER_SUMMARY": "Great! Let me confirm your order {customer_name}. You've ordered: {order_items}. The total is {total} for pickup at {pickup_time}.",
        
        "MODIFICATION_REQUEST": "I understand you'd like to make changes. What would you like to modify in your order?",
        
        "ORDER_CONFIRMATION": "Thank you for your order, {customer_name}! Your order will be ready for pickup at {pickup_time}. The total is {total}.",
        
        "UNCLEAR_INPUT": "I didn't quite catch that. Could you please clarify what you'd like to order?"
    }
    
    @staticmethod
    def get_response(response_type: str, **kwargs) -> str:
        """Get a response template and fill in any provided variables"""
        template = ResponseTemplates.RESPONSES.get(response_type)
        if template and kwargs:
            return template.format(**kwargs)
        return template
