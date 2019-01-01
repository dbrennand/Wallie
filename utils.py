try:
    import subprocess, click, os, requests
    from math import ceil
    from platform import system
    from tqdm import tqdm
    from huepy import yellow
except ImportError as err:
    print(f"Failed to import required modules: {err}")


def download_image(image_url, file_name):
    """Download the users specified image to the project directory.
    Returns:
        file_name string."""
    with requests.get(image_url, stream=True) as resp:
        if ((resp.status_code) == (requests.codes.ok)):
            block_size = 1024
            total_size = int(resp.headers["content-length"])
            try:
                with open(f"{file_name}.jpg", "wb") as f:
                    for chunk in tqdm(iterable=resp.iter_content(block_size), total=ceil(total_size//block_size), unit="KB", unit_scale=True, desc=f"Downloading {file_name}.jpg"):
                        f.write(chunk)
            except IOError:
                click.secho(f"Failed to create {file_name}.jpg", fg="bright_yellow", err=True)
                exit()
        else:
            click.secho(f"{resp.raise_for_status()}", fg="bright_yellow")
            exit()
    click.secho("Download Complete!", fg="bright_yellow")
    return f"{file_name}.jpg"


def present_images(images):
    """Present image choices to the user and request choice.
    Returns:
        user_choice list."""
    for num, item in enumerate(images, 0):
        click.secho(
            f"""Image: {num} -- {item[0]["author_name"]}\nProfile: {item[0]["author_profile"]}\nImage Link: {item[0]["full_image"]}\n""", fg="bright_yellow")
    user_choice = int(input(yellow("Select your preferred image: ")))
    user_choice = images[user_choice]
    return user_choice


def check_os(abs_path):
    """Check the operating system and run the respective desktop setting command
    Returns:
        False: If command fails to set desktop wallpaper.
        True: if the command successfully sets the desktop wallpaper."""
    os_name = system()
    if os_name == "Darwin":
        try:
            SCRIPT = """osascript -e 'tell application "Finder" to set desktop picture to "{abs_path}" as POSIX file'"""
            subprocess.run(SCRIPT.format(abs_path=abs_path), shell=True)
            # return True if the command successfully executes.
            return True
        except subprocess.CalledProcessError as err:
            click.secho(
                f"Failed to set desktop wallpaper with the following error:\n{err}", fg="bright_yellow")
            # return False if the command fails.
            return False
    elif os_name == "Windows":
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)
            # return True if the command successfully executes.
            return True
        except RuntimeError as err:
            click.secho(
                f"Failed to set desktop wallpaper with the following error:\n{err}", fg="bright_yellow")
            # return False if the command fails.
            return False
    elif os_name == "Linux":
        command = get_linux_envrionment()
        if command is not None:
            try:
                subprocess.run(command.format(abs_path=abs_path), shell=True)
                # return True if the command successfully executes.
                return True
            except subprocess.CalledProcessError as err:
                click.secho(
                    f"Failed to set desktop wallpaper with the following error:\n{err}", fg="bright_yellow")
                # return False if the command fails.
                return False
        # If None: get_linux_envrionment() returns None when envrionment cannot be determined.
        else:
            click.secho("Your Linux desktop envrionment is not supported.", fg="bright_yellow")
            # return False if the command fails.
            return False


def get_linux_envrionment():
    """Get the current linux desktop envrionment of the user
    Returns:
        command: The command to set the desktop environment.
    https://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment"""
    if os.environ.get("KDE_FULL_SESSION") == "true":
        command = """
                    qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
                        var allDesktops = desktops();
                        print (allDesktops);
                        for (i=0;i<allDesktops.length;i++) {{
                            d = allDesktops[i];
                            d.wallpaperPlugin = "org.kde.image";
                            d.currentConfigGroup = Array("Wallpaper",
                                                   "org.kde.image",
                                                   "General");
                            d.writeConfig("Image", "file:///{abs_path}")
                        }}
                    '
                """
    elif os.environ.get("DESKTOP_SESSION") == "gnome":
        command = "gsettings set org.gnome.desktop.background picture-uri file://{abs_path}"
    elif os.environ.get("DESKTOP_SESSION") == "Lubuntu":
        command = "pcmanfm -w {abs_path} --wallpaper-mode=fit"
    elif os.environ.get("DESKTOP_SESSION") == "mate":
        command = "gsettings set org.mate.background picture-filename {abs_path}"
    else:
        command = None
    return command
