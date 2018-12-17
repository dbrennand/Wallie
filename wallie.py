try:
    import requests, click, subprocess
    from os.path import abspath
    from huepy import yellow
    from config import UNSPLASH_CLIENT_ID
except ImportError as err:
    print(f"Failed to import modules: {err}")


def parse_resp(json: dict):
    """From JSON resp, collect the top 4 images from results."""
    images = []
    for num, item in enumerate(json["results"], 1):
        image_info = {"author_name": item["user"]["name"], "full_image": item["urls"]["full"], "image_id": item["id"],
                      "author_profile": f"{item['user']['links']['html']}?utm_source=Wallie&utm_medium=referral", "download_location": item["links"]["download_location"]}
        image_list = []
        image_list.append(image_info)
        images.append(image_list)
    return images


def present_images(images):
    """Present image choices to the user and request choice."""
    for num, item in enumerate(images, 0):
        click.secho(
            f"""Image: {num} -- {item[0]["author_name"]}\nProfile: {item[0]["author_profile"]}\nImage Link: {item[0]["full_image"]}\n""", fg="bright_yellow")
    user_choice = int(input(yellow("Select your preferred image: ")))
    user_choice = images[user_choice]
    return user_choice


def trigger_download(download_location):
    """Trigger a download event to Unsplash API.
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


def download_image(image_url, file_name):
    """Download the users specified image to the project directory."""
    subprocess.run(["wget", "-O", f"{file_name}.jpg", f"{image_url}"])
    click.secho("Download Complete!", fg="bright_yellow")
    return f"{file_name}.jpg"


def make_request(api, subject):
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


@click.command()
@click.option("--api", default="unsplash", required=True, show_default=True, help="API to use.", type=str)
@click.argument("subject", default="Space", type=str)
def set(api, subject):
    """Sets the Wallpaper of the device."""
    click.secho(f"Searching {api} for {subject} images...", fg="bright_yellow")
    resp = make_request(api, subject)
    images = parse_resp(resp)
    user_choice = present_images(images)
    trigger_download(user_choice[0]["download_location"])
    file_name = download_image(user_choice[0]["full_image"], subject)
    click.secho(
        f"Attempting to set desktop image to {file_name}", fg="bright_yellow")
    try:
        abs_path = abspath(f"./{file_name}")
        click.secho(f"{abs_path}", fg="bright_yellow")
        SCRIPT = """osascript -e 'tell application "Finder" to set desktop picture to "%s" as POSIX file'"""
        subprocess.run(SCRIPT % abs_path, shell=True)
    except subprocess.CalledProcessError as err:
        click.secho(
            f"Failed to set desktop wallpaper with the following error:\n{err}", fg="bright_yellow")


def wallie_version(ctx, param, value):
    """Prints the version of Wallie."""
    if not value or ctx.resilient_parsing:
        return
    click.secho("Version - 0.1", fg="bright_yellow")
    ctx.exit()


@click.option('--version', "--v", is_flag=True, callback=wallie_version, expose_value=False, is_eager=True)
@click.group()
def main():
    """Entry point for CLI"""
    pass


# Adding Commands to application.
main.add_command(set)
if __name__ == "__main__":
    main()
