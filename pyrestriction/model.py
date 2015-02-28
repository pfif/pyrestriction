from pyrestriction.exceptions import NoNextOperation
# This file defines the model of the application: the bank account and the
# various operations that are on going on it.

class AccountPeriodMixin:
    """
    This mixin compute these numbers for a period:
    - The amount of money on it
    - The amount of money avaliable to the user
    - The amount of money saved this month: money unavaliable to the user but kept on the account at the end of the month
    - The amount of debt: money unavaliable to the user and that is taken away from the account at the end of the period

    Its money_begining_period, regular_income, name, and currency properties must be implemented by each of its subclasses

    It has the operation for its period, although it does not provide any way to add operations.
    Sublasses must, or not, do this bit.

    It is in charge to generate, if it can, the AccountPeriod for the next period
    """
    def __init__(self, operations=None):
        if operations == None:
            self._operations = list()
        else:
            self._operations = operations

    def  _add_amounts(self, debt):
        result = 0
        for operation in self._operations:
            if operation.debt == debt:
                result += operation.amount
        return result
 
    def total(self):
        return self.money_begining_period

    def saved(self):
        return self._add_amounts(False)

    def debt(self):
        return self._add_amounts(True)

    def avaliable(self):
        return self.total() - (self.saved() + self.debt())

    def next(self):
        next_operations = list()
        for op in self._operations:
            try:
                next_op = op.next()
                next_operations.append(next_op)
            except NoNextOperation:
                pass

        return AccountPeriod(self, next_operations)

    @property
    def operations(self):
        return self._operations


class AccountPeriod(AccountPeriodMixin):
    """
    This account period retrieve
    """
    def __init__(self, previous_accountperiod, operations):
        super(AccountPeriod, self).__init__(operations)
        self._previous_accountperiod = previous_accountperiod

    @property
    def money_begining_period(self):
        return (self._previous_accountperiod.total() - self._previous_accountperiod.debt())+self.regular_income

    @property
    def regular_income(self):
        return self._previous_accountperiod.regular_income

    @property
    def name(self):
        return self._previous_accountperiod.name

    @property
    def currency(self):
        return self._previous_accountperiod.currency

class Account(AccountPeriodMixin):
    """
    This is a bank account.
    Various operation are being done with the money it holds.

    An accunt has three simple property :
    - The amount of money currently on
    - The amount of money that enter in it at the end of period
    """
    def __init__(self, current_amount, regular_income, account_name, account_currency):
        super(Account, self).__init__()
        self.money_begining_period = current_amount
        self.regular_income = regular_income
        self.name = account_name
        self.currency = account_currency

    #Operation handling part
    def add_operation(self, operation):
        self.operations.append(operation)
        

class Operation:
    """
    An operation that takes money from the amount avaliable to the user
    If it is a debt, this money must be payed out of the user account.

    Its method "next" is responsible to create the Operation for the next period.
    If there is no next operation, it must raise NoNextOperation.
    """
    def __init__(self, amount, debt = False):
        self._amount = amount
        self._debt = debt

    @property
    def amount(self):
        return self._amount

    @property
    def debt(self):
        return self._debt

class SavingOperation(Operation):
    """Save money during one period"""
    def __init__(self, amount):
        super(SavingOperation, self).__init__(amount)

    def next(self):
        raise NoNextOperation()

class RegularSavingOperation(Operation):
    """Save an amount of money over several periods"""
    def __init__(self, total_amount, nb_period_left, saved_amount):
        self._total_amount = total_amount
        self._nb_period_left = nb_period_left

        saved_this_period = 0
        if self._nb_period_left >= 1 :
            saved_this_period = (total_amount-saved_amount)/self._nb_period_left
        super(RegularSavingOperation, self).__init__(saved_amount + saved_this_period)

    def next(self):
        return RegularSavingOperation(self._total_amount, self._nb_period_left-1, self.amount)

class DebtOperation(Operation):
    """Pay a debt over a number of period"""
    def __init__(self, total_amount, nb_period_left, payed_this_period, payed_amount):
        if not payed_this_period:
            super(DebtOperation, self).__init__((total_amount-payed_amount)/nb_period_left, True)
        else :
            super(DebtOperation, self).__init__(0, True)
        self._total_amount = total_amount
        self._nb_period_left = nb_period_left
        self._payed_amount = payed_amount

    def next(self):
        if self._nb_period_left - 1 >= 1 : 
            return DebtOperation(self._total_amount, self._nb_period_left - 1, False, self._payed_amount + self.amount)
        else:
            raise NoNextOperation()

class RegularPaymentOperation(Operation):
      """Pay the same amount every period"""
      def __init__(self, amount, payed_this_period):
          if not payed_this_period:
              super(RegularPaymentOperation, self).__init__(amount, True)
          else:
              super(RegularPaymentOperation, self).__init__(0, True)
          self._regular_amount = amount

      def next(self):
          return RegularPaymentOperation(self._regular_amount, False)
