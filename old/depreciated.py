def old_unsplash_parse_resp(json: dict):
    """From JSON resp, collect the top 4 images from results.
    NOW Depreciated."""
    images = []
    for num, item in enumerate(json["results"], 1):
        image_info = {"author_name": item["user"]["name"], "full_image": item["urls"]["full"], "image_id": item["id"],
                      "author_profile": f"{item['user']['links']['html']}?utm_source=Wallie&utm_medium=referral", "download_location": item["links"]["download_location"]}
        image_list = []
        image_list.append(image_info)
        images.append(image_list)
    return images

def make_request(api, subject):
    """Old request function. Now using Unsplash wrapper. NOW Depreciated."""
    if api == "unsplash":
        endpoint = "https://api.unsplash.com"
        headers = {"Accept-Version": "v1",
                   "Authorization": f"Client-ID {UNSPLASH_CLIENT_ID}"}
        try:
            if subject is not None:
                endpoint = f"{endpoint}/search/photos"
                resp = requests.get(
                    endpoint, params={"query": subject, "per_page": 4}, headers=headers)
            # else: subject is None
            else:
                endpoint = f"{endpoint}/photos/random"
                resp = requests.get(endpoint, headers=headers)
            if ((resp.status_code) == (requests.codes.ok)):
                return resp.json()
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