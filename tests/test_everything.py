import unittest
from pyrestriction.model import *

class OperationWithNext(Operation):
    def __init__(self, amount, debt):
        super(OperationWithNext, self).__init__(amount, debt)
    
    def next(self):
        raise NoNextOperation()

class AccountPeriodMixinTest(unittest.TestCase):
    """
    This test case test the class Account that is derived from AccountPeriodMixin!
    """

    AMOUNT_ON_ACCOUNT = 10000
    REGULAR_INCOME = 1000
    ACCOUNT_NAME = "Pfif's empty debit account"
    ACCOUNT_CURRENCY = "PND"

    OPERATIONS_SAVED = [500, 1000]
    OPERATIONS_DEBT = [505, 253]

    @staticmethod
    def create_instance():
        instance = Account(AccountPeriodMixinTest.AMOUNT_ON_ACCOUNT , AccountPeriodMixinTest.REGULAR_INCOME, AccountPeriodMixinTest.ACCOUNT_NAME, AccountPeriodMixinTest.ACCOUNT_CURRENCY)
        for op_value in AccountPeriodMixinTest.OPERATIONS_SAVED:
            instance.add_operation(OperationWithNext(op_value, False))
        for op_value in AccountPeriodMixinTest.OPERATIONS_DEBT:
            instance.add_operation(OperationWithNext(op_value, True))
             
        return instance

    def setUp(self):
        self._instance = self.create_instance()
  
    def tearDown(self):
        pass

    def test_total(self):
        """Return the amount of money avaliable at the begining of the month"""
        self.assertEqual(self.AMOUNT_ON_ACCOUNT, self._instance.total())
  
    def test_saved(self):
        """Test that saved() return the right amount of saved money"""
        self.assertEqual(sum(x for x in self.OPERATIONS_SAVED), self._instance.saved())
  
    def test_debt(self):
        """Test that debt() return the right amount of debt money"""
        self.assertEqual(sum(x for x in self.OPERATIONS_DEBT), self._instance.debt())
  
    def test_avaliable(self):
        """Test that avaliable() return the right amount of money avaliable to the user :
        total-(saved+debt)
        """
        self.assertEqual(self.AMOUNT_ON_ACCOUNT - (sum(x for x in self.OPERATIONS_SAVED) + sum(x for x in self.OPERATIONS_DEBT)), self._instance.avaliable())
    
    def test_next(self):
        """Only test that a AccountPeriod is returned"""
        self.assertEqual(type(self._instance.next()), AccountPeriod)

class AccountPeriodTest(unittest.TestCase):
    def setUp(self):
        self._instance_prev = AccountPeriodMixinTest.create_instance()
        self._instance = AccountPeriod(self._instance_prev, [OperationWithNext(500, False)])
  
    def tearDown(self):
        pass

    def test_money_begining_period(self):
        """Test that : the money begining period is rightly computed based on the previous AccountPeriod"""
        self.assertEqual(AccountPeriodMixinTest.AMOUNT_ON_ACCOUNT  - sum(x for x in AccountPeriodMixinTest.OPERATIONS_DEBT) + AccountPeriodMixinTest.REGULAR_INCOME, self._instance.money_begining_period)

    def test_regular_income(self):
        """Test that the regular income is taken from the previous AccountPerdiod"""
        self.assertEqual(AccountPeriodMixinTest.REGULAR_INCOME, self._instance.regular_income)

    def test_name(self):
        """Test that the name is taken from the previous AccountPeriod"""
        self.assertEqual(AccountPeriodMixinTest.ACCOUNT_NAME, self._instance.name)

    def test_currency(self):
        """Test that the currency is taken from the previous AccountPeriod"""
        self.assertEqual(AccountPeriodMixinTest.ACCOUNT_CURRENCY, self._instance.currency)

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
