Pyrestriction
=============

Tell it the amounts that you owe or want to save, and Pyrestriction calculates
how much money is still available.

For example, here's some information that you can provide for an account:

* I want to save £500 this month
* I have a £150 debt that I can pay over three months
* I want to save £1236 this year

Then, when you give it the current amount of money in the account,
Pyrestriction will return the available amount for two months:

```
-------------------
Period : 1
-------------------
Amounts :
Total amount : 20000
Debt amount : 50
Saved amount : 603
Avaliable amount : 19357
-------------------
-------------------
Period : 2
-------------------
Amounts :
Total amount : 19950
Debt amount : 50
Saved amount : 103
Avaliable amount : 19797
-------------------
```

Swell! How does it work?
========================

First, we are quickly going to introduce the terminology required to understand
how the program works, explain how to make account files, and finally show you
how to run the program. Keep reading!

Key Terms
---------

In Pyrestriction, time is split into **periods**. A period's length is as long
as you want it to be: one month, one week, or even changing from one period to
the next. During a period, money is saved and debts are payed.

To describe what will be saved or payed, we use **operations**. The role of an
operation is to pay or save money for one or more period(s). There are several
types of operations, some that simply save or pay money for one period, and some
that save or pay an amount of money over several periods. All of the operations
are presented below.

Installation
------------

Pyrestriction is only compatible with Python 3. To install it, simply run

```
python3 ./setup.py install
```

Tell it the amount that you owe or want to save
-----------------------------------------------

All information about an account is stored in a regular Python file, parsed by
Pyrestriction at runtime.

This file contains 4 variables:

* `NAME`: The name of the account
* `CURRENCY`: A string representing the currency
* `REGULAR_ACCOUNT`: The amount of money added at the end of each period
* `OPERATION`: An iterable returning `Operation`s (it can be a simple `list`)

There are four types of operations. You do not need to import them manually,
because Pyrestriction will do it automatically when parsing the file:

* `SavingOperation`: Save an amount of money this period 
* `DebtOperation`: Pay an amount of money this period
* `SavingRegularOperation`: Save an amount of money over several periods
* `RegularPaymentOperation`: Pay an amount of money each period

To see how to instantiate and use them, please check out the
`pyrestriction/model.py` file and the example account file
`test/example_account.act`.

Run the program
---------------

To run the program, you must provide two arguments to the program:

```
pyrestriction amount_on_account path_to_account_file
```

`amount_on_account` is the total amount of money in your account.
