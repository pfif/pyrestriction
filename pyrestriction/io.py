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

def write_account(account, buffer):
    variable = lambda name, value: "{name} = {value}".format(name=name, value=value)
    variable_string = lambda name, value: variable(name, '"{value}"'.format(value=value))
    print(variable("REGULAR_INCOME", account.regular_income), file=buffer)
    print(variable_string("NAME", account.name), file=buffer)
    print(variable_string("CURRENCY", account.currency), file=buffer)
    print("", file=buffer)
    print(variable("OPERATIONS", "[{operations}]".format(
        operations = ",\n".join(o.__repr__() for o in account.operations)
    )), file=buffer)
