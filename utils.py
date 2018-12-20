try:
    import subprocess, click
    from huepy import yellow
except ImportError as err:
    print(f"Failed to import required modules: {err}")


def download_image(image_url, file_name):
    """Download the users specified image to the project directory."""
    subprocess.run(["wget", "-O", f"{file_name}.jpg", f"{image_url}"])
    click.secho("Download Complete!", fg="bright_yellow")
    return f"{file_name}.jpg"


def present_images(images):
    """Present image choices to the user and request choice."""
    for num, item in enumerate(images, 0):
        click.secho(
            f"""Image: {num} -- {item[0]["author_name"]}\nProfile: {item[0]["author_profile"]}\nImage Link: {item[0]["full_image"]}\n""", fg="bright_yellow")
    user_choice = int(input(yellow("Select your preferred image: ")))
    user_choice = images[user_choice]
    return user_choice
