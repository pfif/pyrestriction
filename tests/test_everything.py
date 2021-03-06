import unittest
from pyrestriction.model import *
from pyrestriction.io import write_account
from io import StringIO

class OperationWithNext(Operation):
    def __init__(self, amount, debt, counter=0):
        super(OperationWithNext, self).__init__(amount, debt)
        self._counter = counter
    
    def next(self):
        if self._counter < 1:
            return OperationWithNext(self.amount, self.debt, self._counter + 1) 
        else:
            raise NoNextOperation()

# TEST FOR THE CLASSES DERIVED FROM AccountPeriodMixin
#
# There are two classes derived from AccountPeriodMixin (Account and AccountPeriod), 
# and those two can be in two modes (Normal and OperationOnly)
#
# To test this, for each classes, we create 3 test case
# - 1 test case for the functions that work the same way for both mode
# - 1 test case to test specific behabior in Normal mode
#
# One last test case is created to test specific behavior on OperationOnly mode for both classes 
#
# All of these classes derives from unittest.TestCase and AccountTestBase

class AccountTestBase:
    """
    Base set up for testing the classes derived from AccountPeriodMixin
    """

    AMOUNT_ON_ACCOUNT = 10000
    REGULAR_INCOME = 1000
    ACCOUNT_NAME = "Pfif's empty debit account"
    ACCOUNT_CURRENCY = "PND"

    OPERATIONS_SAVED = [500, 1000]
    OPERATIONS_DEBT = [505, 253]

    def create_instance(self, amount_on_account):
        instance = Account(amount_on_account, self.REGULAR_INCOME, self.ACCOUNT_NAME, self.ACCOUNT_CURRENCY)
        for op_value in self.OPERATIONS_SAVED:
            instance.add_operation(OperationWithNext(op_value, False))
        for op_value in self.OPERATIONS_DEBT:
            instance.add_operation(OperationWithNext(op_value, True))
             
        return instance

    def setUp_account(self, amount_on_account):
        self._instance = self.create_instance(amount_on_account)
 
    def setUp_accountperiod(self, amount_on_account):
        self._instance_prev = self.create_instance(amount_on_account)
        self._instance = AccountPeriod(self._instance_prev, [OperationWithNext(500, False)])

    def test_next(self):
        """Test that a AccountPeriod is returned, that all the operations have their counter raised, then that no operation is returned"""
        def test_operations_counter(account, counter_nb):
            for op in account.operations:
                self.assertEqual(op._counter, counter_nb) 

        test_operations_counter(self._instance, 0)

        next_instance = self._instance.next()
        self.assertEqual(type(next_instance), AccountPeriod)
        test_operations_counter(next_instance, 1)
        
        last_instance = next_instance.next()
        self.assertEqual(len(last_instance.operations), 0)

class TestBothModeMixin:
    """Add this mixin to a class that test a subclass of AccountPeriodMixin to make it run its tests twice. Once in OperationOnly mode and once in Normal mode"""
    def run(self, *args, **kwargs):
        self._amount_on_account = None
        super(TestBothModeMixin, self).run(*args, **kwargs)

        self._setupfunction = self.AMOUNT_ON_ACCOUNT
        super(TestBothModeMixin, self).run(*args, **kwargs)

class AccountTest(TestBothModeMixin, unittest.TestCase, AccountTestBase):
    """Test Account and AccountPeriodMixin in both mode"""
    def setUp(self):
        self.setUp_account(self._amount_on_account)
  
    def test_saved(self):
        """Test that saved() return the right amount of saved money"""
        self.assertEqual(sum(x for x in self.OPERATIONS_SAVED), self._instance.saved())
  
    def test_debt(self):
        """Test that debt() return the right amount of debt money"""
        self.assertEqual(sum(x for x in self.OPERATIONS_DEBT), self._instance.debt())
  
class AccountNormalModeTest(unittest.TestCase, AccountTestBase):
    """Test Account and AccountPeriodMixin in Normal mode only"""
    def setUp(self):
        self.setUp_account(self.AMOUNT_ON_ACCOUNT)
    
    def test_total(self): 
        """Return the amount of money avaliable at the begining of the month"""
        self.assertEqual(self.AMOUNT_ON_ACCOUNT, self._instance.total())

    def test_avaliable(self):
        """Test that avaliable() return the right amount of money avaliable to the user :
        total-(saved+debt)
        """
        self.assertEqual(self.AMOUNT_ON_ACCOUNT - (sum(x for x in self.OPERATIONS_SAVED) + sum(x for x in self.OPERATIONS_DEBT)), self._instance.avaliable())

class AccountPeriodTest(TestBothModeMixin, unittest.TestCase, AccountTestBase):
    """Test AccountPeriod in both mode"""
    def setUp(self):
        self.setUp_accountperiod(self._amount_on_account) 

    def test_regular_income(self):
        """Test that the regular income is taken from the previous AccountPeriod"""
        self.assertEqual(self.REGULAR_INCOME, self._instance.regular_income)

    def test_name(self):
        """Test that the name is taken from the previous AccountPeriod"""
        self.assertEqual(self.ACCOUNT_NAME, self._instance.name)

    def test_currency(self):
        """Test that the currency is taken from the previous AccountPeriod"""
        self.assertEqual(self.ACCOUNT_CURRENCY, self._instance.currency)

class AccountPeriodNormalModeTest(unittest.TestCase, AccountTestBase):
    """Test AccountPeriod in Normal mode only"""
    def setUp(self):
        self.setUp_accountperiod(self.AMOUNT_ON_ACCOUNT)

    def test_money_begining_period(self):
        """Test that : the money begining period is rightly computed based on the previous AccountPeriod"""
        self.assertEqual(self.AMOUNT_ON_ACCOUNT  - sum(x for x in self.OPERATIONS_DEBT) + self.REGULAR_INCOME, self._instance.money_begining_period)
    

class AccountOperationsOnlyModeTest(unittest.TestCase, AccountTestBase):
    """Test Account and AccountPeriod in OperationOnly mode :
       The objects have not been made aware of how much money is on the account and only serve as a container for the remaining data."""

    def run(self, *args, **kwargs):
        self._setupfunction = "setUp_account"
        super(AccountOperationsOnlyModeTest, self).run(*args, **kwargs)

        self._setupfunction = "setUp_accountperiod"
        super(AccountOperationsOnlyModeTest, self).run(*args, **kwargs)

    def setUp(self):
        self.__getattribute__(self._setupfunction)(None)

    def test_total(self):
        """Calculation is impossible due to missing data, OperationOnlyMode exception is raised"""
        with self.assertRaises(OperationsOnlyMode):
            self._instance.total()
  
    def test_avaliable(self):
        """Calculation is impossible due to missing data, OperationOnlyMode exception is raised"""
        with self.assertRaises(OperationsOnlyMode):
            self._instance.avaliable()
    

class SavingOperationTest(unittest.TestCase):
    AMOUNT_SAVING = 100

    def setUp(self):
        self._instance = SavingOperation(self.AMOUNT_SAVING)
    
    def test_amountscurrent(self):
        """Test that this is not a debt and that the amount is correct"""
        self.assertFalse(self._instance.debt)
        self.assertEqual(self._instance.amount, self.AMOUNT_SAVING)

    def test_amountsnext(self):
        """Test that this raise a NoNextOperation exception"""
        with self.assertRaises(NoNextOperation):
            self._instance.next()

    def test_repr(self):
        """Test that the representation value is correct and allows the object to be recreated when executed"""
        self.assertEqual(
            self._instance.__repr__(),
            "SavingOperation(amount = {AMOUNT_SAVING})".format(
                AMOUNT_SAVING=self.AMOUNT_SAVING
            )
        )
    
class DebtOperationTest(unittest.TestCase):
    TOTAL_AMOUNT = 500
    NB_PERIOD_LEFT = 5
    AMOUNT_ALREADY_PAYED = 58

    def run(self, *args, **kwargs):
        self._payed = False
        super(DebtOperationTest, self).run(*args, **kwargs)

        self._payed = True
        super(DebtOperationTest, self).run(*args, **kwargs)

    def setUp(self):
        self._instance = DebtOperation(self.TOTAL_AMOUNT, self.NB_PERIOD_LEFT, self._payed, self.AMOUNT_ALREADY_PAYED)
    
    def compute_current_amount(self):
        if(self._payed):
            return 0
        else:
            return (self.TOTAL_AMOUNT-self.AMOUNT_ALREADY_PAYED)/self.NB_PERIOD_LEFT
    
    def test_amountscurrent(self):
        """Test that this is a debt and that the amount is correctly divided"""
        self.assertTrue(self._instance.debt)
        self.assertEqual(self.compute_current_amount(), self._instance.amount)

    def test_amountsnext(self):
        """Test that this is a debt and that the amount is the same"""
        next_instance = self._instance.next()
        self.assertTrue(next_instance.debt)
        self.assertEqual((self.TOTAL_AMOUNT-(self.AMOUNT_ALREADY_PAYED+self.compute_current_amount()))/(self.NB_PERIOD_LEFT-1), next_instance.amount)

    def test_raisenonextoperation(self):
        """Test that when the debt is payed, no Operation are yield"""
        last_instance = self._instance.next().next().next().next()
        with self.assertRaises(NoNextOperation):
            last_instance.next() 

    def test_repr(self):
        """Test that the representation value is correct and allows the object to be recreated when executed"""
        self.assertEqual(
            self._instance.__repr__(),
            "DebtOperation(total_amount = {TOTAL_AMOUNT}, nb_period_left = {NB_PERIOD_LEFT}, payed_this_period = {payed}, payed_amount = {AMOUNT_ALREADY_PAYED})".format(
                TOTAL_AMOUNT=self.TOTAL_AMOUNT, 
                NB_PERIOD_LEFT = self.NB_PERIOD_LEFT,
                payed=self._payed, 
                AMOUNT_ALREADY_PAYED=self.AMOUNT_ALREADY_PAYED
            )
        )
        

class RegularPaymentOperationTest(unittest.TestCase):
    AMOUNT = 100
    
    def run(self, *args, **kwargs):
        self._payed = False
        super(RegularPaymentOperationTest, self).run(*args, **kwargs)

        self._payed = True
        super(RegularPaymentOperationTest, self).run(*args, **kwargs)


    def setUp(self):
        self._instance = RegularPaymentOperation(self.AMOUNT, self._payed)
    
    def test_amountscurrent(self):
        """Test that this is a debt and that the amount is correct, if it is a payed or unpayed amount"""
        self.assertTrue(self._instance.debt)
        if(self._payed):
            self.assertEqual(self._instance.amount, 0)
        else:
            self.assertEqual(self._instance.amount, self.AMOUNT)

    def test_amountsnext(self):
        """Test that this is a debt and that the amount is the same"""
        next_instance = self._instance.next()
        self.assertEqual(next_instance.amount, self.AMOUNT)
        self.assertTrue(next_instance.debt)

    def test_repr(self):
        """Test that the representation value is correct and allows the object to be recreated when executed"""
        self.assertEqual(
            self._instance.__repr__(),
            "RegularPaymentOperation(regular_amount = {AMOUNT}, payed_this_period = {payed})".format(
                AMOUNT=self.AMOUNT, 
                payed=self._payed, 
            )
        )
        

class RegularSavingOperationTest(unittest.TestCase):
    TOTAL_AMOUNT = 5000
    NB_PERIOD_LEFT = 5
    ALREADY_SAVED = 656
    def setUp(self):
        self._instance = RegularSavingOperation(self.TOTAL_AMOUNT, self.NB_PERIOD_LEFT, self.ALREADY_SAVED)
    
    def compute_current_amount(self):
        return self.ALREADY_SAVED + (self.TOTAL_AMOUNT-self.ALREADY_SAVED)/self.NB_PERIOD_LEFT 

    def test_amountscurrent(self):
        """Test that this isn't a debt and that the amount are correctly divided"""
        self.assertFalse(self._instance.debt)
        self.assertEqual(self._instance.amount, self.compute_current_amount())

    def test_amountsnext(self):
        """Test that this isn't a debt and that the amount is the same"""
        next_instance = self._instance.next()
        self.assertFalse(next_instance.debt)
        self.assertEqual(next_instance.amount, self.compute_current_amount()+(self.TOTAL_AMOUNT-(self.compute_current_amount()))/(self.NB_PERIOD_LEFT-1))
    def test_amountszeroperiodleft(self):
        """Test that the amount is fully saved at the end of the operation and beyond"""
        def test_equal_totalamount(amount):
            self.assertEqual(amount, self.TOTAL_AMOUNT)
            
        zeroperiodleft_instance = self._instance.next().next().next().next().next()
        test_equal_totalamount(zeroperiodleft_instance.amount)
        test_equal_totalamount(zeroperiodleft_instance.next().amount)
    
    def test_repr(self):
        """Test that the representation value is correct and allows the object to be recreated when executed"""
        self.assertEqual(
            self._instance.__repr__(),
            "RegularSavingOperation(total_amount = {TOTAL_AMOUNT}, nb_period_left = {NB_PERIOD_LEFT}, saved_amount = {ALREADY_SAVED})".format(
                TOTAL_AMOUNT=self.TOTAL_AMOUNT, 
                NB_PERIOD_LEFT = self.NB_PERIOD_LEFT, 
                ALREADY_SAVED = self.ALREADY_SAVED
            )
        )

class WriteAccountTest(unittest.TestCase):
    REGULAR_INCOME = 1000
    NAME = "Write account test"
    CURRENCY = "EUR"

    OPERATION_AMOUNT = 500

    def setUp(self):
        self._account = Account(1000, self.REGULAR_INCOME, self.NAME, self.CURRENCY)
        self._account.add_operation(OperationWithNext(self.OPERATION_AMOUNT, True))
        self._account.add_operation(OperationWithNext(self.OPERATION_AMOUNT, False))

    def test_formataccount(self):
        formated_account = StringIO() 
        write_account(self._account, formated_account)
        self.assertEqual(
            formated_account.getvalue(),
            'REGULAR_INCOME = {REGULAR_INCOME}\nNAME = "{NAME}"\nCURRENCY = "{CURRENCY}"\n\nOPERATIONS = [OperationWithNext(amount = {AMOUNT}, debt = True, counter = 0),\nOperationWithNext(amount = {AMOUNT}, debt = False, counter = 0)]\n'.format(
                REGULAR_INCOME = self.REGULAR_INCOME,
                NAME = self.NAME,
                CURRENCY = self.CURRENCY,
                AMOUNT = self.OPERATION_AMOUNT
            )
        )
