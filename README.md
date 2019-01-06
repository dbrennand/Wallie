# Wallie
Wallie is a CLI which can set your device desktop wallpaper!
![Wallie Demo](Wallie_Demo.gif)

## Currently Supported APIs
* Unsplash API
* Pexels API
* Pixabay API

## OSs Supported
* Windows, Mac, Linux support below (UNTESTED)

## Supported Linux desktop environments (UNTESTED).
* KDE, Gnome, Lubuntu, mate.

## Usage
![Wallie help](Wallie_help.png)

## TODO
* Add support for more APIs.
* Add support for other OSs (Windows specifically) ✅
* Exception handling for download_image(). ✅
* Remove wget dependancy and add progress bar. ✅
* Correct colours on progress bar. ✅

## Dependancies
Wallie currently requires:
```
[packages]
requests = "*"
click = "*"
colorama = "*"
pypexels = "*"
pyunsplash = "*"
python-pixabay = "*"

[requires]
python_version = "3.7"
```

Install all dependancies using the following command:
```
pipenv install
```

## Authors -- Contributors

* **Daniel Brennand** - *Author* - [Dextroz](https://github.com/Dextroz)

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 License - see the [LICENSE](LICENSE) for details.

## Acknowledgments

* Requests created by [Kenneth Reitz (kennethreitz)](https://github.com/kennethreitz) and respective contributors.
* Pypexels and Pyunsplash wrappers by [salvoventura](https://github.com/salvoventura) and respective contributors.

