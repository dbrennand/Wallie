try:
    import requests, click
    from config import CLIENT_ID
except ImportError as err:
    print(f"Failed to import modules: {err}")


def make_request(api, subject):
    headers = {"Accept-Version": "v1", "Authorization": f"Client-ID {CLIENT_ID}"}
    if api == "unsplash":
        endpoint = "https://api.unsplash.com"
        try:
            if subject not None:
                endpoint = f"{endpoint}/search/photos"
                resp = requests.get(endpoint, params={"query": subject}, headers=headers)
            # If subject is other than None
            else:
                endpoint = f"{endpoint}/photos/random"
                resp = requests.get(endpoint, headers=headers)
            if ((resp.status_code) == (requests.codes.ok)):
                return resp.json()
            else:
                # Raise the error if status code is not ok ie evaluates to True.
                resp.raise_for_status()
        except requests.exceptions.TooManyRedirects:
            click.secho("Request exceeded the acceptable number of redirects.", fg="bright_yellow")
        except requests.exceptions.Timeout:
            click.secho("Request timed out.", fg="bright_yellow")
        except requests.exceptions.HTTPError as err:
            click.secho(f"The following HTTPError occured {err}", fg="bright_yellow")

@click.command()
@click.option("--api", default="unsplash", required=True, show_default=True, help="API to use.", type=str)
@click.argument("subject", default="Space", type=str)
def set(api, subject):
    """Sets the Wallpaper of the device"""
    click.secho(f"Searching {api} for {subject} images...", fg="bright_yellow")
    resp = make_request(api, subject)
    click.secho(resp, fg="bright_yellow")

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
