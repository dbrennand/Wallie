try:
    import requests, click
    from config import CLIENT_ID
except ImportError as err:
    print(f"Failed to import modules: {err}")

def parse_resp(json: dict):
    """From JSON resp, collect the top 4 images from results"""
    images = []
    for num, item in enumerate(json["results"], 1):
        image_info = {"author_name": item["user"]["name"], "author_profile": f"{item['user']['links']['html']}?utm_source=your_app_name&utm_medium=referral", "full_image": item["urls"]["full"]} 
        images.append(image_info)
    return images

def present_images(images: dict):
    for num, images in enumerate(images, 1):
        click.secho(f"""Image: {num} -- By {images["author_name"]} -- Profile: {images["author_profile"]}""", fg="bright_yellow")

def make_request(api, subject):
    headers = {"Accept-Version": "v1", "Authorization": f"Client-ID {CLIENT_ID}"}
    if api == "unsplash":
        endpoint = "https://api.unsplash.com"
        try:
            if subject != None:
                endpoint = f"{endpoint}/search/photos"
                resp = requests.get(endpoint, params={"query": subject, "per_page": 4}, headers=headers)
            # else: subject is None
            else:
                endpoint = f"{endpoint}/photos/random"
                resp = requests.get(endpoint, headers=headers)
            if ((resp.status_code) == (requests.codes.ok)):
                return resp.json()
            else:
                # Raise the error if status code is not ok ie evaluates to True.
                click.secho(resp.raise_for_status(), err=True)
        except requests.exceptions.TooManyRedirects:
            click.secho("Request exceeded the acceptable number of redirects.", fg="bright_yellow", err=True)
        except requests.exceptions.Timeout:
            click.secho("Request timed out.", fg="bright_yellow", err=True)
        except requests.exceptions.HTTPError as err:
            click.secho(f"The following HTTPError occured {err}", fg="bright_yellow", err=True)

@click.command()
@click.option("--api", default="unsplash", required=True, show_default=True, help="API to use.", type=str)
@click.argument("subject", default="Space", type=str)
def set(api, subject):
    """Sets the Wallpaper of the device"""
    click.secho(f"Searching {api} for {subject} images...", fg="bright_yellow")
    resp = make_request(api, subject)
    images = parse_resp(resp)
    present_images(images)


def wallie_version(ctx, param, value):
    """Prints the version of Wallie"""
    if not value or ctx.resilient_parsing:
        return
    click.secho("Version - 0.1", fg="bright_yellow")
    ctx.exit()

@click.option('--version', "--v", is_flag=True, callback=wallie_version, expose_value=False, is_eager=True)
@click.group()
def main():
    pass

# Adding Commands to application.
main.add_command(set)
if __name__ == "__main__":
    main()
