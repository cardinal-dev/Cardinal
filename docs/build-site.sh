#!/bin/bash

# Build Cardinal site
# falcon78921

# Make sure you have at least Ruby 2.1.0 installed. We recommend using rvm.
source /etc/profile
gem install bundler
bundle install
bundle exec jekyll serve --host 0.0.0.0

