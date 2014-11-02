import argparse 
from pyrestriction.model import Account, SavingOperation, SavingRegularOperation, DebtOperation, RegularPaymentOperation
from pyrestriction.views import CLIView

AMOUNT_ARG = "amount_on_account"
ACCOUNT_ARG = "account_file"

def parse_account(current_amount, account_string):
    """Parse an account from an ACT file. The ACT file must contain four variables : NAME, REGULAR_INCOME, CURRENCY, OPERATIONS"""
    glob = {'SavingOperation':SavingOperation, 'SavingRegularOperation':SavingRegularOperation, 'DebtOperation':DebtOperation, 'RegularPaymentOperation':RegularPaymentOperation}
    loc = dict()
    exec(account_string, glob, loc)
    account = Account(current_amount, loc['REGULAR_INCOME'], loc['NAME'], loc['CURRENCY'])
    for operation in loc['OPERATIONS']:
        account.add_operation(operation)

    return account

def parse():
    argpars = argparse.ArgumentParser(prog="pyrestriction", description="Tell it the amounts that you owe or want to save, and it will compute how much money is avaliable to you.", epilog="You must set the current operations restraining money from your direct usage in an account file. You can find an exemple of account file in tests/account_exemple.act.")
    argpars.add_argument(AMOUNT_ARG ,  type = int, help = "The amount of money currently on the account")
    argpars.add_argument(ACCOUNT_ARG, type = argparse.FileType('r'), help = "the file containing the account of which you want to show the avaliable funds")
    
    args = vars(argpars.parse_args())
    account = parse_account(args[AMOUNT_ARG], args[ACCOUNT_ARG].read())
    view = CLIView()
    
    view.render(account)
