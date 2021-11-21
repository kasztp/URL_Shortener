# URL Shortener API

URL Shortener api experiment with Flask


Endpoints:

/ --> API imput/output examples.

/v1/url-management/shorten --> URL Shortener.

/v1/url-management/route --> Basic routing (redirect) to stored URLs based on the shortened value.


Initial setup:
1. Set DEBUG = False in config.py.
2. Set DB URI in config.py (or use sqlite as fellback)
3. Prepare DB with Flask migrate


Demo: TBD


## Authors

* **Peter Kaszt** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

