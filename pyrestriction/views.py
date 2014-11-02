#This file contains all the views that can display accounts

SEPARATOR = "-------------------"
def _surround_separators(func):
    def function(*args, **kwargs):
        print(SEPARATOR)
        func(*args, **kwargs)
        print(SEPARATOR)
    return function
        
class CLIView(object):

    @_surround_separators
    def _render_header_account(self, accountperiod):
        print("Account : {account.name}".format(account = accountperiod))
        
    @_surround_separators
    def _render_period(self, period_number, accountperiod):
        #Print period number 
        print("Period : ", end = "")
        if(period_number == 0):
            print ("Current")
        else:
            print(period_number)

        print(SEPARATOR)

        #Print avaliable money
        print("Amounts :")
        print("Total amount : {0}".format(accountperiod.total()))
        print("Debt amount : {0}".format(accountperiod.debt()))
        print("Saved amount : {0}".format(accountperiod.saved()))
        print("Avaliable amount : {0}".format(accountperiod.avaliable()))

    def render(self, accountperiod):
        self._render_header_account(accountperiod)
        
        for i in range(1,3):
            self._render_period(i, accountperiod)
            accountperiod = accountperiod.next()


