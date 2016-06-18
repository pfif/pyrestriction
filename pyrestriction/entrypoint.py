from argparse import ArgumentParser, FileType
from pyrestriction.views import AccountView, MessageView
from pyrestriction.io import parse_account, write_account

AMOUNT_ARG = "amount_on_account"
ACCOUNT_ARG = "account_file"


def write_account_to_file(account, file):
    file.seek(0)
    write_account(account, file)
    file.truncate()


class PyrestrictionSubparserBase(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(PyrestrictionSubparserBase, self).__init__(*args, **kwargs)
        self.add_argument(
            ACCOUNT_ARG,
            type=FileType('r+'),
            help="the file containing the account of which you want to show the avaliable funds"
        )


def entrypoint():
    # Main ArgumentParser
    argparser = ArgumentParser(prog="pyrestriction", description="Tell it the amounts that you owe or want to save, and it will compute how much money is avaliable to you.", epilog="You must set the current operations restraining money from your direct usage in an account file. You can find an exemple of account file in tests/account_exemple.act.")
    subparser = argparser.add_subparsers(title="Commands", parser_class=PyrestrictionSubparserBase)

    # Available subcommand
    def subcommand_available(args):
        account = parse_account(args[AMOUNT_ARG], args[ACCOUNT_ARG].read())
        view = AccountView(account)
        return view
    available_parser = subparser.add_parser(
        "available", description="Show how much money is available on your account."
    )
    available_parser.add_argument(
        AMOUNT_ARG, type=int, help="The amount of money currently on the account"
    )
    available_parser.set_defaults(func=subcommand_available)

    # Format subcommand
    def subcommand_format(args):
        account = parse_account(None, args[ACCOUNT_ARG].read())
        write_account_to_file(account, args[ACCOUNT_ARG])
        view = MessageView("format", {"filename": args[ACCOUNT_ARG].name})
        return view
    format_parser = subparser.add_parser("format", description="Format the account file")
    format_parser.set_defaults(func=subcommand_format)

    # Endperiod subcommand
    def subcommand_endperiod(args):
        account = parse_account(None, args[ACCOUNT_ARG].read())
        account = account.next()
        write_account_to_file(account, args[ACCOUNT_ARG])
        view = MessageView("endperiod", {"account_name": account.name,
                                         "filename": args[ACCOUNT_ARG].name})
        return view
    format_parser = subparser.add_parser(
        "endperiod", description="End the period and write the new values to the account file"
    )
    format_parser.set_defaults(func=subcommand_endperiod)

    args = argparser.parse_args()
    dict_args = vars(args)
    try:
        view = args.func(dict_args)
        view.render()
    except AttributeError:
        argparser.print_help()

if __name__ == "__main__":
    entrypoint()
