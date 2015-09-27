from pyrestriction.model import Account, SavingOperation, RegularSavingOperation, DebtOperation, RegularPaymentOperation

def parse_account(current_amount, account_string):
    """Parse an account from an ACT file. The ACT file must contain four variables : NAME, REGULAR_INCOME, CURRENCY, OPERATIONS"""
    glob = {'SavingOperation':SavingOperation, 'RegularSavingOperation':RegularSavingOperation, 'DebtOperation':DebtOperation, 'RegularPaymentOperation':RegularPaymentOperation}
    loc = dict()
    exec(account_string, glob, loc)
    account = Account(current_amount, loc['REGULAR_INCOME'], loc['NAME'], loc['CURRENCY'])
    for operation in loc['OPERATIONS']:
        account.add_operation(operation)

    return account
