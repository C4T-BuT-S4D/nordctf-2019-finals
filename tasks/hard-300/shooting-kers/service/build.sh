#!/bin/bash

PHP_FILENAME=index.php
HTML_FILENAME=dump.html

VLD_PARAMS=-dvld.active=1 -dvld.execute=0 -dvld.dump_paths=0 -dvld.verbosity=0

python3 generate_auto.php > "$PHP_FILENAME"
php "$VLD_PARAMS" "$PHP_FILENAME" 2>&1 | python3 generate_html.py > "$HTML_FILENAME"

mv "$PHP_FILENAME" "$HTML_FILENAME" web/
