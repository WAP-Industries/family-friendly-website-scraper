__import__("sys").dont_write_bytecode = True

from scraper import Scraper

def main() -> str:
    args = __import__("argparser").Parser.parse_args()

    config = {
        "Tags": args.tags,
        "Exclude": args.exclude
    }
    if any(map(lambda x:"*" in x, config.values())):
        res = Scraper.LoadConfig()
        if not res[0]:
            return Scraper.Error(f"Unable to load configurations as {res[1]}")
        config = {i:[y for x in config[i] for y in (Scraper.Config[i] if x=="*" else [x])] for i in config}

    return f"=== Fetch Results ===\n\n{Scraper.Scrape(*config.values(), args.page, args.batchsize, args.random, args.saveconfig)}"

if __name__=="__main__":
    print(f"\n{main()}\n")