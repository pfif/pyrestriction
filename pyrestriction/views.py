# This file contains all the views that can display accounts

SEPARATOR = "-------------------"


def _surround_separators(func):
    def function(*args, **kwargs):
        print(SEPARATOR)
        func(*args, **kwargs)
        print(SEPARATOR)
    return function


class AccountView(object):
    def __init__(self, accountperiod, show_detail_operations):
        self._accountperiod = accountperiod
        self._show_detail_operations = show_detail_operations

    def _render_operation(self, operation_list):
        if self._show_detail_operations:
            for operation in operation_list:
                print("    " + str(operation))

    @_surround_separators
    def _render_header_account(self, accountperiod):
        print("Account : {account.name}".format(account=accountperiod))

    @_surround_separators
    def _render_period(self, period_number, accountperiod):
        operations_debt = [op for op in accountperiod.operations if op.debt]
        operations_saved = [op for op in accountperiod.operations if not op.debt]

        # Print period number
        print("Period : ", end="")
        if(period_number == 0):
            print("Current")
        else:
            print(period_number)

        print(SEPARATOR)

        # Print avaliable money
        print("Amounts :")
        print("Total amount : {0}".format(accountperiod.total()))
        print("Debt amount : {0}".format(accountperiod.debt()))
        self._render_operation(operations_debt)
        print("Saved amount : {0}".format(accountperiod.saved()))
        self._render_operation(operations_saved)
        print("Avaliable amount : {0}".format(accountperiod.avaliable()))

    def render(self):
        self._render_header_account(self._accountperiod)

        accountperiod = self._accountperiod
        for i in range(2):
            self._render_period(i, accountperiod)
            accountperiod = accountperiod.next()


class MessageView():
    messages = {"format": "Formated {filename}.",
                "endperiod": "All the operations on {account_name} have been passed to the next period and written to {filename}."}

    def __init__(self, key, format_arguments):
        self._key = key
        self._format_arguments = format_arguments

    def render(self):
        print(self.messages[self._key].format(**self._format_arguments))
