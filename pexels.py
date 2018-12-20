try:
    from pypexels import PyPexels
    from config import PEXELS_API_KEY
except ImportError as err:
    print(f"Failed to import modules: {err}")


def pexels_parse_resp(subject):
    """From Pexels API RESP, collect the top 4 images from results."""
    py_pexel = PyPexels(api_key=PEXELS_API_KEY)
    results = py_pexel.search(query=subject, per_page=4)
    images = []
    for num, item in enumerate(results.entries, 1):
        image_info = {"author_name": item.photographer, "full_image": item.src["original"], "image_id": item.id,
                      "author_profile": item.photographer_url}
        image_list = []
        image_list.append(image_info)
        images.append(image_list)
    return images
