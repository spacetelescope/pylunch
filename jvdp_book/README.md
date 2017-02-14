This directory stores the content for the PyLunch sessions on the "Python Data Science Handbook" by Jake VanderPlas.

The physical (or e-)book is available [from O'Reilly](http://shop.oreilly.com/product/0636920034919.do) or your favorite bookseller.  However, all the content for the book is also available on [its github repository](https://github.com/jakevdp/PythonDataScienceHandbook).  So there is no need to purchase the book unless you prefer it in that format.

## If you have not cloned the pylunch repository before

If you have not done so already, you will need to have [anaconda]() installed.  Then you can follow these instructions to get the repository in a proper state to follow along:

1. Check if git is installed by typing ``git`` into the command line.  If you get "command not found" or similar, you need to do the next step.
2. If not, do ``conda install git``
3. Once git is installed, go to some place where you'll find it later (perhaps your home directory), and do ``git clone https://github.com/spacetelescope/pylunch.git``.  This will create a directory called "pylunch".
4. ``cd pylunch``
5. ``git submodule init``
6. ``git submodule update``

You should now have both the pylunch-specific materials *and* the notebooks for the text.


## If you already have the pylunch repository

If you have previously cloned the PyLunch repository using git, you should only need to issue the following commands:

```
git submodule init
git submodule update
```

Which will pull down a copy of the book.


## Updating for future sessions

At the beginning of each session, you should ``cd pylunch`` and then do ``git pull``, which should grab new materials for the next session.  If you get any errors, call the moderators over for help!
