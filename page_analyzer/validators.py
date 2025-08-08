import validators


def validate_url(url_string):
    if not url_string:
        return 'URL обязателен'
    if len(url_string) > 255:
        return 'URL превышает 255 символов'
    if not validators.url(url_string):
        return 'Некорректный URL'
    return None