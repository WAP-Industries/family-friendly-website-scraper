import argparse

Parser = argparse.ArgumentParser()

Parser.add_argument(
    "--tags", 
    nargs="+", 
    help="Tags to filter doujins by", 
    required=True
)
Parser.add_argument(
    "--exclude", 
    nargs="+", 
    default=[], 
    help="Filter out all the nasty shit"
)
Parser.add_argument(
    "--page", 
    type=int, 
    default=1, 
    help="Website page number"
)
Parser.add_argument(
    "--batchsize", 
    type=int, 
    default=None, 
    help="Sets the max number of results"
)
Parser.add_argument(
    "--random", 
    action="store_true", 
    help="Picks a random doujin from the fetched results"
)