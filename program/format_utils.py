"""
    Given the current price and the match price, return a string with proper formatting
    with number of
"""
def format_price(current, match):

    current_string = f"{current}"
    match_string = f"{match}"

    # Check for decimals in the match, and get the number of decimals
    if '.' in match_string:
        decimals = len(match_string.split('.')[1])
        current_string = f"{current:.{decimals}f}"
        current_string = current_string[:]
        return current_string
    else:
        return f"{int(current)}"