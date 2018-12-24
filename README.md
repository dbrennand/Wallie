# Wallie
Pronounced "Wall-E", Wallie is a CLI which can set your device desktop wallpaper!
![Wallie Demo](Wallie_Demo.gif)

## Currently Supported APIs
* Unsplash API
* Pexels API.

## OSs Supported
* Windows, Mac, see linux support below!

### Supported Linux desktop envrionments.
* KDE, Gnome, Lubuntu, mate.

## TODO
* Add support for other OSs (Windows specifically) ✅
* Add support for more APIs.
* Exception handling for download_image(). 
* Remove wget dependancy and add progress bar.

## Dependancies
Wallie currently requires:
* wget
```
requests = "*"
click = "*"
colorama = "*"
huepy = "*"
pypexels = "*"
pyunsplash = "*"

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

