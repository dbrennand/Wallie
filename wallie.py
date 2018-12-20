try:
    # File imports.
    import click, subprocess
    from os.path import abspath
    # Other file imports.
    from config import UNSPLASH_CLIENT_ID
    from utils import download_image, present_images
    from unsplash import unsplash_parse_resp, unsplash_trigger_download
    from pexels import pexels_parse_resp
except ImportError as err:
    print(f"Failed to import modules: {err}")


@click.command()
@click.option("--api", default="unsplash", required=True, show_default=True, help="API to use.", type=str)
@click.argument("subject", default="Space", type=str)
def set(api, subject):
    """Sets the Wallpaper of the device. TODO: Add support for other OSs"""
    click.secho(f"Searching {api} for {subject} images...", fg="bright_yellow")
    if api == "unsplash":
        images = unsplash_parse_resp(subject)
        user_choice = present_images(images)
        unsplash_trigger_download(user_choice[0]["download_location"])
    elif api == "pexels":
        images = pexels_parse_resp(subject)
        user_choice = present_images(images)
    file_name = download_image(user_choice[0]["full_image"], subject)
    click.secho(
        f"Attempting to set desktop image to {file_name}", fg="bright_yellow")
    try:
        abs_path = abspath(f"./{file_name}")
        SCRIPT = """osascript -e 'tell application "Finder" to set desktop picture to "%s" as POSIX file'"""
        subprocess.run(SCRIPT % abs_path, shell=True)
        click.secho("Wallpaper set successfully!", fg="bright_yellow")
    except subprocess.CalledProcessError as err:
        click.secho(
            f"Failed to set desktop wallpaper with the following error:\n{err}", fg="bright_yellow")


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
