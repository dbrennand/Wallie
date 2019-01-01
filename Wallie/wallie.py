try:
    # File imports.
    import click
    from os.path import abspath
    # Other file imports.
    from utils import download_image, present_images, check_os
    from unsplash import unsplash_parse_resp, unsplash_trigger_download
    from pexels import pexels_parse_resp
except ImportError as err:
    print(f"Failed to import modules: {err}")


@click.command()
@click.option("--api", default="unsplash", required=True, show_default=True, help="API to use.", type=str)
@click.argument("subject", default="Space", type=str)
def set(api, subject):
    """Sets the Wallpaper of the device."""
    click.secho(f"Searching {api} for {subject} images...", fg="bright_yellow")
    if api == "unsplash":
        images = unsplash_parse_resp(subject)
        user_choice = present_images(images)
        unsplash_trigger_download(user_choice[0]["download_location"])
    elif api == "pexels":
        images = pexels_parse_resp(subject)
        user_choice = present_images(images)
    else:
        click.secho("Invalid API option.", fg="bright_yellow")
        exit()
    file_name = download_image(user_choice[0]["full_image"], subject)
    click.secho(
        f"Attempting to set desktop image to {file_name}", fg="bright_yellow")
    abs_path = abspath(f"./{file_name}")
    condition = check_os(abs_path)
    if condition is False:
        exit()
    else:
        click.secho("Wallpaper set successfully!", fg="bright_yellow")


def wallie_version(ctx, param, value):
    """Prints the version of Wallie."""
    if not value or ctx.resilient_parsing:
        return
    click.secho("Version - 0.2", fg="bright_yellow")
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
