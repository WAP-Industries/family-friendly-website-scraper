import argparse

Parser = argparse.ArgumentParser()

Parser.add_argument(
    "--tags", 
    nargs="+", 
    help="doujin tags to search for", 
    required=True
)
Parser.add_argument(
    "--exclude", 
    nargs="+", 
    default=[], 
    help="nasty shit to filter out"
)
Parser.add_argument(
    "--page", 
    type=int, 
    default=1, 
    help="page number of search results"
)
Parser.add_argument(
    "--batchsize", 
    type=int, 
    default=None, 
    help="max number of results"
)
Parser.add_argument(
    "--random", 
    action="store_true", 
    help="pick a random doujin from the fetched results"
)