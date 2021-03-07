#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__version__ = "$version: 00.01$"
__revised__ = "$revised: 2021-02-28 13:23:24$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
This little app makes updating the __revised__ variable easy...
"""

GENRES = [
    'Action',
    'Adventure',
    'Alternate history',
    'Anthology',
    'Autobiography',
    'Biography',
    'Business/economics',
    'Chick lit',
    'Classic',
    'Crime',
    'Dark Erotica',
    'Dark Fantasy',
    'Detective & Mystery',
    'Diary',
    'Drama',
    'Dystopian',
    'Erotic Fiction',
    'Fairytale',
    'Fantasy',
    'Graphic Audio',
    'High Fantasy',
    'Historical fiction',
    'History',
    'Horror',
    'Humor',
    'LGBTQ+',
    'Mystery',
    'Paranormal romance',
    'Philosophy',
    'Political thriller',
    'Romance',
    'Satire',
    'Science',
    'Science Fiction',
    'Science Fiction & Fantasy',
    'Self help',
    'Short story',
    'Sports and leisure',
    'Suspense',
    'Thriller',
    'Travel',
    'True crime',
    'Urban Fantasy',
    'Western',
    'Young adult'
]

CHAPTER_LIST = [
    "Based on mp3 length",
    "Fixed 3 minutes",
    "Fixed 10 minutes",
    "Fixed 15 minutes",
    "Fixed 30 minutes",
    "Fixed 45 minutes",
    "Fixed 60 minutes"
]

if __name__ == '__main__':
    GENRES.sort()
    import pprint

    pprint.pprint(list(set(GENRES)))
