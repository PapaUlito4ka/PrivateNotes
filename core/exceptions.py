

def handle_error(context: dict, e: Exception):
    context['errors'] = str(e)
