from argparse import ArgumentParser, FileType
from pyrestriction.views import CLIView
from pyrestriction.io import parse_account

AMOUNT_ARG = "amount_on_account"
ACCOUNT_ARG = "account_file"

class PyrestrictionSubparserBase(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(PyrestrictionSubparserBase, self).__init__(*args, **kwargs)
        self.add_argument(ACCOUNT_ARG, type = FileType('r'), help = "the file containing the account of which you want to show the avaliable funds")

def entrypoint():
    #Main ArgumentParser
    argparser = ArgumentParser(prog="pyrestriction", description="Tell it the amounts that you owe or want to save, and it will compute how much money is avaliable to you.", epilog="You must set the current operations restraining money from your direct usage in an account file. You can find an exemple of account file in tests/account_exemple.act.")
    subparser = argparser.add_subparsers(title="Commands", parser_class = PyrestrictionSubparserBase)

    #Available subcommand
    def subcommand_view(args):
        account = parse_account(args[AMOUNT_ARG], args[ACCOUNT_ARG].read())
        view = CLIView()
        view.render(account)
    available_parser = subparser.add_parser("available", description="Show how much money is available on your account.")
    available_parser.add_argument(AMOUNT_ARG,  type = int, help = "The amount of money currently on the account")
    available_parser.set_defaults(func = subcommand_view)
    
    args = argparser.parse_args()
    dict_args = vars(args)
    try:
        args.func(dict_args)
    except AttributeError:
        argparser.print_help()

if __name__ == "__main__":
    entrypoint()
