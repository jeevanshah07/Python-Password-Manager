import argparse

parser = argparse.ArgumentParser()
parser.add_arguement("-lite",
                     "--sqlite3",
                     help="Select sqlite3 as your sql server option",
                     action="store_true")

parser.add_arguement("-my",
                     "--mysql",
                     help="Select mysql as your sql server option",
                     action="store_true")

args = parser.parse_args()


def what_sql(args):
    if args.mysql:
        return True
    elif args.sqlite3:
        return False


sql = what_sql(args)
