try:
    import click, requests
    from config import UNSPLASH_CLIENT_ID
    from pyunsplash import PyUnsplash
except ImportError as err:
    print(f"Failed to import modules: {err}")


def unsplash_parse_resp(subject):
    """From Unsplash API, collect the top 4 images from results.
    Params:
        subject: string: The subject to use for the image search.
    Returns:
        images: nested dict."""
    py_un = PyUnsplash(api_key=UNSPLASH_CLIENT_ID)
    search = py_un.search("photos", query=subject, per_page=4)
    images = []
    for num, item in enumerate(search.entries, 1):
        image_info = {"author_name": item.body["user"]["name"], "full_image": item.body["urls"]["full"], "image_id": item.id,
                      "author_profile": f"{item.body['user']['links']['html']}?utm_source=Wallie&utm_medium=referral", "download_location": item.link_download_location}
        image_list = []
        image_list.append(image_info)
        images.append(image_list)
    return images


def unsplash_trigger_download(download_location):
    """Trigger a download event to Unsplash API.
    Params:
        download_location: string: The download url provided and required by unsplash API.
    More Info: https://medium.com/unsplash/unsplash-api-guidelines-triggering-a-download-c39b24e99e02"""
    try:
        resp = requests.get(download_location, headers={
                            "Accept-Version": "v1", "Authorization": f"Client-ID {UNSPLASH_CLIENT_ID}"})
        if ((resp.status_code) == (requests.codes.ok)):
            pass
        else:
            # Raise the error if status code is not ok ie evaluates to True.
            click.secho(f"{resp.raise_for_status()}",
                        err=True, fg="bright_yellow")
    except requests.exceptions.TooManyRedirects:
        click.secho("Request exceeded the acceptable number of redirects.",
                    fg="bright_yellow", err=True)
    except requests.exceptions.Timeout:
        click.secho("Request timed out.", fg="bright_yellow", err=True)
    except requests.exceptions.HTTPError as err:
        click.secho(
            f"The following HTTPError occured {err}", fg="bright_yellow", err=True)
