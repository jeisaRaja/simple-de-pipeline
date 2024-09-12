import pandas as pd


def categorize_shipping(ship):
    if pd.isna(ship):
        return "Unknown"
    ship = ship.lower()
    if "free" in ship:
        return "Free"
    if "standard" in ship:
        return "Standard"
    if "usd" or "cad" in ship:
        return "Paid"
    return "Unknown"


def handle_manufacturer(value):
    if pd.isna(value):
        return "Unknown"
    value = value.lower()
    if "year" in value:
        return "Unknown"
    return value.title()


def handle_is_available(value):
    avail = [
        "yes",
        "true",
        "in stock",
        "more on the way",
        "special order",
        "32 available",
        "7 available",
    ]
    lower_val = value.lower()
    if lower_val in avail:
        return True
    return False


def handle_condition(value):
    value = value.lower()

    if "new" in value:
        return "New"
    elif "used" in value or "pre-owned" in value:
        return "Used"
    elif (
        "refurbished" in value
        or "seller refurbished" in value
        or "manufacturer refurbished" in value
    ):
        return "Refurbished"
    else:
        return "Unknown"
