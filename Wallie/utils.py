try:
    # File imports.
    import subprocess, click, os, requests, ctypes
    from platform import system, dist
    from colorama import Fore
except ImportError as err:
    print(f"Failed to import required modules: {err}")


def handle_err(error):
    """
    Present errors which occur.
        :param error: The string of the error which occurs.
    """
    click.secho(f"An error occured: {error}", fg="bright_yellow", err=True)
    exit()


def download_image(image_url, file_name):
    """
    Download the users specified image to the project directory.
        :param image_url: The string url for the image to be downloaded.
        :param file_name: The string file_name to use for the downloaded image.
        :rtype: The string of the file_name downloaded.
        :except resp.raise_for_status: Occurs if HTTP resp_code is not 200.
    """

    def write_file(file_name, resp, bar):
        """
        Writes the image file to disk.
            :param file_name: The string file_name to use for the downloaded image.
            :param resp: The requests Response object.
            :param bar: The click.progressbar object or type(None): no progress bar.
            :except IOError: Occurs if .jpg file fails to be written to disk.
        """
        try:
            with open(f"{file_name}.jpg", "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
                    if bar is None:
                        pass
                    else:
                        bar.update(len(chunk))
        except IOError:
            handle_err(f"Failed to create {file_name}.jpg")

    # Start of download_image()
    with requests.get(image_url, stream=True) as resp:
        if (resp.status_code) == (requests.codes.ok):
            # Check for content-length header or transfer-encoding
            # From: https://github.com/requests/requests/issues/4925
            is_chunked = resp.headers.get("transfer-encoding", "") == "chunked"
            content_length = resp.headers.get("content-length")
            if not is_chunked and content_length.isdigit():
                total_size = int(content_length)
                with click.progressbar(
                    length=total_size,
                    show_eta=True,
                    show_percent=True,
                    fill_char=">",
                    label=f"Downloading {file_name}.jpg",
                    bar_template=click.style(
                        "%(label)s  [%(bar)s]  %(info)s", fg="bright_yellow"
                    ),
                ) as bar:
                    # See write_file above.
                    write_file(file_name, resp, bar)
            else:
                # Fails to get content-length. No progress bar as progress bar requires total_size.
                write_file(file_name, resp, None)
        else:
            handle_err(f"Donwload image request failed: {resp.raise_for_status()}")
    click.secho("Download Complete!", fg="bright_yellow")
    return f"{file_name}.jpg"


def present_images(images):
    """
    Present image choices to the user and request the user to choose one.
        :param images: A list containing data on the images retrieved.
        :rtype user_choice: A dict containing data on the users chosen image.
    """
    for num, item in enumerate(images, 0):
        click.secho(
            f"""Image: {num} -- {item["author_name"]}\nProfile: {item["author_profile"]}\nImage Link: {item["full_image"]}\n""",
            fg="bright_yellow",
        )
    # Formats prompt all yellow coloured.
    user_choice = int(
        click.prompt(
            click.style("Select your preferred image: ", fg="bright_yellow"),
            prompt_suffix="",
        )
    )
    user_choice = images[user_choice]
    return user_choice


def get_linux_environment():
    """
    Determine the users current Linux desktop environment.
        :rtype command: The string command for the specific desktop environment or type(None).
    """
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
    elif os.environ.get("DESKTOP_SESSION") == "Lubuntu":
        lubuntu_version = float(dist()[1])
        if lubuntu_version <= 18.04:
            command = "pcmanfm -w {abs_path}"
        elif lubuntu_version > 18.04:
            command = "pcmanfm-qt -w {abs_path}"
    elif os.environ.get("DESKTOP_SESSION") == "ubuntu":
        command = (
            "gsettings set org.gnome.desktop.background picture-uri file://{abs_path}"
        )
    elif os.environ.get("DESKTOP_SESSION") == "mate":
        command = "gsettings set org.mate.background picture-filename {abs_path}"
    else:
        command = None
    return command


def check_os(abs_path):
    """
    Determine the users operating system and run the respective desktop command.
        :param abs_path: The string PATH to the downloaded image.
        :except subprocess.CalledProcessError: Occurs when MacOS script or Linux command fails to set wallpaper.
        :except Unknown Windows Exception: Requires looking into. Occurs when Windows command fails to set wallpaper.
    """
    os_name = system()
    if os_name == "Darwin":
        try:
            SCRIPT = """osascript -e 'tell application "Finder" to set desktop picture to "{abs_path}" as POSIX file'"""
            subprocess.run(SCRIPT.format(abs_path=abs_path), shell=True)
        except subprocess.CalledProcessError as err:
            handle_err(f"Failed to set desktop wallpaper: {err}")
    elif os_name == "Windows":
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)
        except:
            # TODO Check what expection occurs here.
            handle_err(f"Failed to set desktop wallpaper for Windows.")
    elif os_name == "Linux":
        command = get_linux_environment()
        if command is not None:
            try:
                subprocess.run(command.format(abs_path=abs_path), shell=True)
            except subprocess.CalledProcessError as err:
                handle_err(f"Failed to set desktop wallpaper: {err}")
        # If None: get_linux_environment() returns None when desktop envrionment cannot be determined.
        else:
            handle_err("Your Linux desktop envrionment is not supported.")


def apply_wallpaper(user_choice, file_name):
    """
    Apply the wallpaper for the downloaded image.
        :param user_choice: A dict containing data on the users chosen image.
        :param file_name: The string file_name to use for the downloaded image.
    """
    file_name = download_image(user_choice["full_image"], file_name)
    click.secho(f"Attempting to set desktop image to {file_name}", fg="bright_yellow")
    # Fetch the absolute PATH to the image on disk.
    abs_path = os.path.abspath(f"./{file_name}")
    check_os(abs_path)
    click.secho("Wallpaper set successfully!", fg="bright_yellow")
