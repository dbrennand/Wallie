try:
    import subprocess, click
except ImportError:
    print("Failed to import required modules for utils.py")


def download_image(image_url, file_name):
    """Download the users specified image to the project directory."""
    subprocess.run(["wget", "-O", f"{file_name}.jpg", f"{image_url}"])
    click.secho("Download Complete!", fg="bright_yellow")
    return f"{file_name}.jpg"
