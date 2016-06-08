import hashlib


# Generate hash for title
def get_hash(title):
    hash_object = hashlib.sha256(title.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


# Compress and clean the title
def compress(title):
    f_title = '' .join(e for e in (title.lower().replace('\\em', '').replace('{', '').replace('}', '').replace(
        '.', '').replace('\BBOQ', '').replace('\BBCQ', '').replace('\Bem', '').strip()) if e.isalnum())
    if f_title.isdigit():
        return
    return f_title
