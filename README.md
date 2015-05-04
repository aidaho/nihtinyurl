NIH TinyURL - painfully imitative URL shortener
===============================================

Written on the course of weekend as a test assignment for Umbrella Corp.

The goal of this software is to provide a URL shortener with some twists.

Which are:
*   Keywords (short keys) are imported from text files
*   A decent attempt to use relevant keyword per supplied URL is made

### Installation
    Activate your [virtualenv](https://virtualenv.pypa.io/) and run the following from the project root:
*   Install requirements: `pip install -r requirements/all.txt`
*   Create DB: `./manage.py syncdb`
*   Import some wordlist: `./manage.py import_shortcuts nihtinyurl/fixtures/words-tiny.txt`
*   Launch test server: `./manage.py runserver`
*   You're done! Now go visit http://127.0.0.1:8000/

### Testing
*   Run `./manage.py test`.
