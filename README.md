Pyrestriction
=============
Tell it the amounts that you owe or want to save, and it will compute how much money is avaliable to you.

For exemple, here is the data you can input about an account :

* I want to save £500 this month
* I have a £150 debt that I can pay over three month
* I want to save £1236 over a year

Then, when you give it the current amount of money on the account, it will return the avaliable amount for two months :

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


Swell ! How does it work ?
==========================

We are first quickly going to introduce notions required to understand how the program works, then explain how to make account files, finally show you how to run the program. Follow the guide!

Notions
-------

In pyrestriction, time is splited in **periods**.
A period's lenght is as long as you want it to be : One month, one week or even unequal lenght from a period to another.
During a period, money is saved and debt are payed.

To describe what shall be saved or payed, we use **operations**. The role of an operation is to pay or save money for one or more period(s).
There are several type of operations, some that simply save or pay money for one period, some that save or pay an amount of money over several periods.
All the operations are presented bellow.

Installation
------------

Pyrestriction is only compatible with Python 3. To install it, simply run

```
python3 ./setup.py install
```

Tell it the amount that you owe or want to save
-----------------------------------------------

All informations about an account are stored in a regular Python file, parsed by Pyrestriction at runtime.

This file contains 4 variables :

* ```NAME``` : The Name of the account
* ```CURENCY``` : A string representing the currency
* ```REGULAR_ACCOUNT``` : The amount of money added at the end of each period
* ```OPERATION``` : An iterable returning ```Operation```s (it can be a simple ```list```)

There are four types of operations. You do not need to import, for pyrestriction will do it when parsing the file :

* ```SavingOperation``` : Save an amount of money this period 
* ```DebtOperation``` : Pay an amount of money this period
* ```SavingRegularOperation```: Save an amount of money over several periods
* ```RegularPaymentOperation``` : Pay an amount of money each period

To see how to instantiate and use them, please check out the ```pyrestriction/model.py``` file and the exemple account file ````test/exemple_account.act```.

Run the program
---------------

To run the program, you must provide two arguments to the program :

```
pyrestriction amount_on_account path_to_account_file
```

```Amount on account``` is the total amount on your account.
