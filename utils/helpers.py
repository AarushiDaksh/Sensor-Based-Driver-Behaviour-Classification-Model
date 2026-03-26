def format_int(value):
    if value is None:
        return "N/A"
    return f"{int(value):,}"