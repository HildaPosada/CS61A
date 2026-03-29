from __future__ import annotations

class Transaction:
    def __init__(self, id: int, before: int, after: int):
        self.id = id
        self.before = before
        self.after = after

    def changed(self) -> bool:
        """Return whether the transaction resulted in a changed balance."""
        return self.before != self.after        

    def report(self) -> str:
        """Return a string describing the transaction.

        >>> Transaction(3, 20, 10).report()
        '3: decreased 20->10'
        >>> Transaction(4, 20, 50).report()
        '4: increased 20->50'
        >>> Transaction(5, 50, 50).report()
        '5: no change'
        """
        msg: str = 'no change'
        if self.changed():
            verb: str = 'increased' if self.after > self.before else 'decreased'
            msg = verb + ' ' + str(self.before) + '->' + str(self.after)
        return str(self.id) + ': ' + msg

class BankAccount:
    """A bank account that tracks its transaction history.

    >>> a = BankAccount('Eric')
    >>> a.deposit(100)    # Transaction 0 for a
    100
    >>> b = BankAccount('Erica')
    >>> a.withdraw(30)    # Transaction 1 for a
    70
    >>> a.deposit(10)     # Transaction 2 for a
    80
    >>> b.deposit(50)     # Transaction 0 for b
    50
    >>> b.withdraw(10)    # Transaction 1 for b
    40
    >>> a.withdraw(100)   # Transaction 3 for a
    'Insufficient funds'
    >>> len(a.transactions)
    4
    >>> len([t for t in a.transactions if t.changed()])
    3
    >>> for t in a.transactions:
    ...     print(t.report())
    0: increased 0->100
    1: decreased 100->70
    2: increased 70->80
    3: no change
    >>> b.withdraw(100)   # Transaction 2 for b
    'Insufficient funds'
    >>> b.withdraw(30)    # Transaction 3 for b
    10
    >>> for t in b.transactions:
    ...     print(t.report())
    0: increased 0->50
    1: decreased 50->40
    2: no change
    3: decreased 40->10
    """

    # *** YOU NEED TO MAKE CHANGES IN SEVERAL PLACES IN THIS CLASS ***

    def __init__(self, account_holder: str):
        self.balance: int = 0
        self.holder = account_holder
        self.transactions = []   # ✅ NEW

    def deposit(self, amount: int) -> int:
        before = self.balance
        self.balance += amount
        after = self.balance

        t = Transaction(len(self.transactions), before, after)
        self.transactions.append(t)

        return self.balance

    def withdraw(self, amount: int) -> int | str:
        before = self.balance

        if amount > self.balance:
            after = self.balance   # no change
            t = Transaction(len(self.transactions), before, after)
            self.transactions.append(t)
            return 'Insufficient funds'

        self.balance -= amount
        after = self.balance

        t = Transaction(len(self.transactions), before, after)
        self.transactions.append(t)

        return self.balance


class Email:
    """An email has the following instance attributes:

        msg (str): the contents of the message
        sender (Client): the client that sent the email
        recipient_name (str): the name of the recipient (another client)
    """
    def __init__(self, msg: str, sender, recipient_name: str):
        self.msg = msg
        self.sender = sender
        self.recipient_name = recipient_name

class Server:
    """Each Server has one instance attribute called clients that is a
    dictionary from client names to client objects.

    >>> s = Server()
    >>> # Dummy client class implementation for testing only
    >>> class Client:
    ...     def __init__(self, server, name):
    ...         self.inbox = []
    ...         self.server = server
    ...         self.name = name
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> s.register_client(a) 
    >>> s.register_client(b)
    >>> len(s.clients)  # we have registered 2 clients
    2
    >>> all([type(c) == str for c in s.clients.keys()])  # The keys in self.clients should be strings
    True
    >>> all([type(c) == Client for c in s.clients.values()])  # The values in self.clients should be Client instances
    True
    >>> new_a = Client(s, 'Alice')  # a new client with the same name as an existing client
    >>> s.register_client(new_a)
    >>> len(s.clients)  # the key of a dictionary must be unique
    2
    >>> s.clients['Alice'] is new_a  # the value for key 'Alice' should now be updated to the new client new_a
    True
    >>> e = Email("I love 61A", b, 'Alice')
    >>> s.send(e)
    >>> len(new_a.inbox)  # one email has been sent to new Alice
    1
    >>> type(new_a.inbox[0]) == Email  # a Client's inbox is a list of Email instances
    True
    """
    def __init__(self):
        self.clients = {}

    def send(self, email: Email):
        self.clients[email.recipient_name].inbox.append(email)

    def register_client(self, client):
        self.clients[client.name] = client


class Client:
    def __init__(self, server: Server, name: str):
        self.inbox = []
        self.server = server
        self.name = name
        server.register_client(self)

    def compose(self, message: str, recipient_name: str):
        email = Email(message, self, recipient_name)
        self.server.send(email)


class Mint:
    present_year = 2021

    def __init__(self):
        self.update()

    def create(self, coin_class):
        return coin_class(self.year)

    def update(self):
        self.year = Mint.present_year


class Coin:
    cents = None

    def __init__(self, year):
        self.year = year

    def worth(self):
        age = Mint.present_year - self.year
        extra = max(0, age - 50)
        return self.cents + extra


class Nickel(Coin):
    cents = 5


class Dime(Coin):
    cents = 10