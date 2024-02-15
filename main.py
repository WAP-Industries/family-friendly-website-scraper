__import__("sys").dont_write_bytecode = True

from scraper import Scraper
from argparser import Parser

def main():
    args = Parser.parse_args()
    print(f"\n===Fetch Results===\n\n{Scraper.Scrape(args.tags, args.exclude, args.page, args.batchsize, args.random)}\n")

if __name__=="__main__":
    main()