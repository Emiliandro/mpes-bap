from flask import jsonify, request
from markupsafe import escape
from datetime import datetime 

class APIMain():
    def __init__(self,message_service):
        self.message_service = message_service
        self.date_format = "%Y-%m-%d"
    
    def get_by_id(self,request):
        message_id = escape(request.json['message_id'])
        message = self.message_service.get_message_by_id(message_id=message_id)
        if message is None:
            return jsonify({'error': f'Message with ID {message_id} not found'}), 404
        return jsonify(message)
    
    def get_by_category(self,request):
        category = escape(request.json['category'])
        message = self.message_service.get_message_by_category(category=category)
        if message is None:
            return jsonify({'error': f'Message with category {category} not found'}), 404
        return jsonify(message)
    
    def get_between_date(self,request):
        from_date = escape(request.json['from_date'])
        until_date = escape(request.json['until_date'])
        validated = {
            'from_date':datetime.strptime(from_date, self.date_format),
            'until_date':datetime.strptime(until_date, self.date_format) }    
        message = self.message_service.get_all_messages_between_dates(from_date=validated['from_date'],to_date=validated['until_date'])
        if message is None:
            return jsonify({'error': f'Message with between dates {from_date} and {until_date} not found'}), 404
        return jsonify(message)
    
    def get_category_between_date(self,request):
        from_date = escape(request.json['from_date'])
        until_date = escape(request.json['until_date'])
        validated = {
            'category': escape(request.json['category']),
            'from_date':datetime.strptime(from_date, self.date_format),
            'until_date':datetime.strptime(until_date, self.date_format) }

        message = self.message_service.get_messages_between_dates_with_category(category=validated['category'],from_date=validated['from_date'],to_date=validated['until_date'])
        
        if message is None:
            return jsonify({'error': f'Message with between dates {from_date} and {until_date} not found'}), 404
        return jsonify(message)

    def add_message(self,request):
        title = escape(request.json['title'])
        description = escape(request.json['description'])
        source = escape(request.json['source'])
        category = escape(request.json['category'])
        published_at = escape(request.json['published_at'])
        message = self.message_service.create_message(title, description, source, category, published_at)
        return jsonify(message)

    def update_message(self,request,message_id):
        title = escape(request.json['title'])
        description = escape(request.json['description'])
        source = escape(request.json['source'])
        published_at = escape(request.json['published_at'])
        category = escape(request.json['category'])
        message = self.message_service.update_message(message_id, title, description, source, category, published_at)
        return f"Message {request.json['source']} updated"
