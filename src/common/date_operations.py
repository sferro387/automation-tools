from datetime import datetime, timedelta

def get_next_friday():
    today = datetime.now()
    days_until_friday = (4 - today.weekday()) % 7  # Friday is weekday 4
    next_friday = today + timedelta(days=days_until_friday)
    return next_friday.strftime('%m/%d')

def load_and_format_template(template_path, recipient_name):
    with open(template_path, 'r') as file:
        template = file.read()
    return template.replace('{{date}}', get_next_friday()) \
                   .replace('{{recipient_name}}', recipient_name)