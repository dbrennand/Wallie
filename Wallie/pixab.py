try:
    # File imports.
    from pixabay import Image

    # Other file imports.
    from config import PIXABAY_API_KEY
    from random import randint, choice
    from utils import handle_err
except ImportError as err:
    print(f"Failed to import modules: {err}")

def randomize_query():
    """
    Randomize query search
    note that some of the queries probably has less than 10 pages
        probably need to do a bit research before adding a new query
        to this list.
    :rtype: string: The subject to use for the image search.
    """
    queries = ["bird","flower","cat",
               "dog", "computer", "abstract", "magic"]

    return choice(queries)

def pixabay_parse_resp(subject):
    """From Pixabay API RESP, collect the top 4 images from results.
    Params:
        subject: string: The subject to use for the image search.
    Returns:
        images: list."""
    pix = Image(PIXABAY_API_KEY)
    if subject is not None:
        resp = pix.search(q=subject, per_page=4, image_type="photo")
    else:
        # give more randomized image selections
        resp = pix.search(q=randomize_query(), per_page=4,
                          image_type="photo", page=randint(1, 10))
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
