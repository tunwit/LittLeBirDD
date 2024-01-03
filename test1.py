from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        print(result.scheme)
        print(result.netloc)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Example usage:
url_to_check = "fg"
if is_valid_url(url_to_check):
    print(f"{url_to_check} looks like a valid URL.")
else:
    print(f"{url_to_check} is not a valid URL.")