try:
    # File imports.
    from pixabay import Image

    # Other file imports.
    from config import PIXABAY_API_KEY
    from utils import handle_err
except ImportError as err:
    print(f"Failed to import modules: {err}")


def pixabay_parse_resp(subject):
    """From Pexels API RESP, collect the top 4 images from results.
    Params:
        subject: string: The subject to use for the image search.
    Returns:
        images: list."""
    pix = Image(PIXABAY_API_KEY)
    if subject is not None:
        resp = pix.search(q=subject, per_page=4, image_type="photo")
    else:
        # Carry out default search. No random endpoint for pixabay API.
        resp = pix.search(per_page=4, image_type="photo")
    images = []
    try:
        for num, item in enumerate(resp["hits"], 1):
            image_info = {
                "author_name": item["user"],
                "full_image": item["largeImageURL"],
                "image_id": item["id"],
                "author_profile": f"https://pixabay.com/en/users/{item['user_id']}",
            }
            images.append(image_info)
        return images
    except AttributeError as err:
        handle_err(
            f"Failed to parse pixabay resp object: {err}\nCheck that your API_KEYs are setup correctly."
        )
