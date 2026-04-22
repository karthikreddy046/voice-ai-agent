def detect_language(text):
    # very naive logic for now
    # will replace with proper model later

    if any(char in text for char in "अआइई"):
        return "hindi"
    elif any(char in text for char in "அஆஇ"):
        return "tamil"
    else:
        return "english"