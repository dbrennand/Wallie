try:
    # File imports.
    from pypexels import PyPexels

    # Other file imports.
    from config import PEXELS_API_KEY
    from utils import handle_err
except ImportError as err:
    print(f"Failed to import modules: {err}")


def pexels_parse_resp(subject):
    """
    From Pexels API resp, collect the top 4 images from results.
        :param subject: The subject to be used for the image search or type(None). If None, random photos are fetched.
        :rtype images: A list containing data on the fetched images.
        :except AttributeErrror: Occurs when resp fails to fetch images and enumerate cannot parse resp.
    """
    py_pexel = PyPexels(api_key=PEXELS_API_KEY)
    if subject is not None:
        resp = py_pexel.search(query=subject, per_page=4)
    else:
        resp = py_pexel.random(per_page=4)
    images = []
    try:
        for num, item in enumerate(resp.entries, 1):
            image_info = {
                "author_name": item.photographer,
                "full_image": item.src["original"],
                "image_id": item.id,
                "author_profile": item.photographer_url,
            }
            images.append(image_info)
        return images
    except AttributeError as err:
        handle_err(
            f"Failed to parse pexels resp object: {err}\nCheck that your API_KEYs are setup correctly."
        )
