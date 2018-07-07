#!/bin/bash

# Cardinal Continuous Integration using Nette
# falcon78921

# This script is designed to test the quality of the Cardinal PHP codebase. 

/home/travis/.config/composer/vendor/nette/code-checker/code-checker -d /var/www/html/
/home/travis/.config/composer/vendor/nette/code-checker/code-checker -d /var/www/html/assets/templates
/home/travis/.config/composer/vendor/nette/code-checker/code-checker -d /var/www/html/includes
/home/travis/.config/composer/vendor/nette/code-checker/code-checker -d /var/www/html/includes/functions
/home/travis/.config/composer/vendor/nette/code-checker/code-checker -d /var/www/html/scripts
