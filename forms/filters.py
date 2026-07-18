async def filter_length_text(text: str, min: int, max: int):
    if len(text) < min:
        return f'Минимальное количество символов: {min}'
    if len(text) > max:
        return f'Максимальное количество символов: {max}'
    return None

async def filter_only_number(text: str):
    if not text.isdigit():
        return f'Допускаются только числовые значения'
    return None