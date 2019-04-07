try:
    # File imports.
    import requests
    from pyunsplash import PyUnsplash

    # Other file imports.
    from config import UNSPLASH_CLIENT_ID
    from utils import handle_err
except ImportError as err:
    print(f"Failed to import modules: {err}")


def unsplash_parse_resp(subject):
    """From Unsplash API, collect the top 4 images from results.
    Params:
        subject: string: The subject to use for the image search.
    Returns:
        images: list.
    Exceptions:
        TypeError: Occurs when resp fails to provide required data."""
    py_un = PyUnsplash(api_key=UNSPLASH_CLIENT_ID)
    images = []
    if subject is not None:
        resp = py_un.search("photos", query=subject, per_page=4)
    else:
        resp = py_un.photos(type_="random", count=4)
    # Gather data from resp object.
    try:
        for num, item in enumerate(resp.entries, 1):
            image_info = {
                "author_name": item.body["user"]["name"],
                "full_image": item.body["urls"]["full"],
                "image_id": item.id,
                "author_profile": f"{item.body['user']['links']['html']}?utm_source=Wallie&utm_medium=referral",
                "download_location": item.link_download_location,
            }
            images.append(image_info)
        return images
    except AttributeError as err:
        handle_err(
            f"Failed to parse unsplash resp object: {err}\nCheck that your API_KEYs are setup correctly."
        )


def unsplash_trigger_download(download_location):
    """Trigger a download event to Unsplash API.
    Params:
        download_location: string: The download url provided and required by unsplash API.
    More Info: https://medium.com/unsplash/unsplash-api-guidelines-triggering-a-download-c39b24e99e02"""
    try:
        resp = requests.get(
            download_location,
            headers={
                "Accept-Version": "v1",
                "Authorization": f"Client-ID {UNSPLASH_CLIENT_ID}",
            },
        )
        if (resp.status_code) == (requests.codes.ok):
            pass
        else:
            # Raise the error if status code is not ok ie evaluates to True.
            handle_err(f"Unsplash trigger download failed: {resp.raise_for_status()}")
    except requests.exceptions.TooManyRedirects as err:
        handle_err(f"Unsplash trigger download failed: {err}")
    except requests.exceptions.Timeout as err:
        handle_err(f"Unsplash trigger download failed: {err}")
    except requests.exceptions.HTTPError as err:
        handle_err(f"Unsplash trigger download failed: {err}")
