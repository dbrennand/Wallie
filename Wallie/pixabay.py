try:
    import python_pixabay
    from config import PIXABAY_API_KEY
except ImportError as err:
    print(f"Failed to import required modules: {err}")


def pixabay_parse_resp(subject):
    """From Pexels API RESP, collect the top 4 images from results.
    Params:
        subject: string: The subject to use for the image search.
    Returns:
        images: nested dict."""
    pix = python_pixabay.Pixabay(api_key=PIXABAY_API_KEY)
    search = pix.image_search(q=subject, per_page=4, image_type="photo")
    images = []
    for num, item in enumerate(search["hits"], 1):
        image_info = {"author_name": item["user"], "full_image": item["largeImageURL"], "image_id": item["id"], "author_profile": f"https://pixabay.com/en/users/{item['user_id']}"}
        image_list = []
        image_list.append(image_info)
        images.append(image_list)
    return images
