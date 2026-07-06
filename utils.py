def clean_text(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def clean_number(value):
    if value is None:
        return None

    try:
        value = str(value).replace(",", "").strip()

        if value == "":
            return None

        return float(value)

    except ValueError:
        return None