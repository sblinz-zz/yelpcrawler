# The Everything Pin

## Project Description

A front-end Google maps interface which allows the user to drop a pin in any location and receive >local information and statistics.
This can include everything from restaurants and points of interest to housing, crime, and education statistics.

The back-end is based on a Python crawler and parser connected to a PostgreSQL database.

## Notes

This project was started as an excuse to develop my SQL skills and learn some new Python tricks and libraries, especially web crawling.
For this reason, we sometimes choose to crawl and parse even in cases where an API exists (e.g., Yelp) and write SQL queries directly instead of
relying on an ORM.

## Features

We start with the simple case of just capturing restaurant information, which we do by crawling Yelp search results.