## Kaggle-query

### purpose

make it cool and interesting to find a dataset for my next data project

### notes

current state - May 22 24

last week we tested the following idea:

can we create embeddings from dataset descriptions then perform nearest neighbors search on an embedded user query?

and we found, yes we can.

next steps:

we'll embed "all" the descriptions and store them. there are lots of them, so we need to consider:

- filtering out junk descriptions (too short, duplicated, etc.)
- storing them - could we save them as a numpy array? yes but we want to explore better options
- before we start embedding, we should cost it out to avoid being surprised by the open ai bill.

once we have created and organized embeddings, we can work on the user interface.

- it'll be a CLI tool - we'll use the `click` library to set it up as such
- we need to write a comprehensive query function that the user will interact with
- we'll test it locally
- then put it in PyPi, a package repository.


list of convenience features to implement later:

- add a filter for size e.g. don't allow extremely large datasets to be returned (or make the size a parameter that can be set by the user) 
- download the dataset if the user accepts it. (this will require the user have kaggle api keys (i think))
- automatically create a new folder with a git repository for the dataset

