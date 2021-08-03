# Write your code here
import random
import sqlite3


def luhn_algorithm(base):
    double_value = []
    for i, value in enumerate(base):
        value = int(value)
        # double odd
        double_value.append(value * 2) if (i + 1) % 2 != 0 else double_value.append(value)
    # subtract the item great than 9
    subtract_9 = list(map(lambda x: x - 9 if x > 9 else x, double_value))
    # get the sum of list
    _sum = sum(subtract_9)

    # remainder with 10
    if _sum % 10 == 0:
        return 0
    else:
        return 10 - _sum % 10


class SimpleBank:
    menu1 = [
        {
            "id": 1,
            "text": 'Create an account'
        },
        {
            "id": 2,
            "text": "Log into account"
        },
        {
            "id": 0,
            "text": "Exit"
        }
    ]

    menu2 = [
        {
            "id": 1,
            "text": 'Balance'
        },
        {
            "id": 2,
            "text": "Add income"
        },
        {
            "id": 3,
            "text": "Do transfer"
        },
        {
            "id": 4,
            "text": "Close account"
        },
        {
            "id": 5,
            "text": "Log out"
        },
        {
            "id": 0,
            "text": "Exit"
        }
    ]
    identify_base = random.randint(100000000, 999999999)
    account = []
    conn = None
    cur = None

    def __init__(self):
        self.conn = sqlite3.connect("card.s3db", timeout=10)
        self.cur = self.conn.cursor()

        exists = self.table_is_exists()
        if len(list(exists)) <= 0:
            self.create_database_table()

    def table_is_exists(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='card'"
        return self.cur.execute(sql)

    def create_database_table(self):
        sql = "create table card(id integer primary key, number text, pin text, balance integer default 0)"
        self.cur.execute(sql)
        self.conn.commit()

    def print_menu1(self):
        for item in self.menu1:
            print(f"{item['id']}. {item['text']}")

    def print_menu2(self):
        for item in self.menu2:
            print(f"{item['id']}. {item['text']}")

    def create_account(self):
        self.identify_base += 1
        card_num = f"400000{self.identify_base}"

        check_sum = luhn_algorithm(card_num)
        card_num = card_num + str(check_sum)
        pin = '{:04}'.format(random.randint(0, 9999))

        sql = f"insert into card values ({random.randint(0, 99999)}, {card_num}, {pin}, 0)"
        self.cur.execute(sql)
        self.conn.commit()

        print("Your card has been created")
        print("Your card number:")
        print(card_num)
        print("Your card PIN:")
        print(pin)

    def find_by_card_num(self, card_num):
        sql = f"select * from card where number={card_num}"
        self.cur.execute(sql)
        return self.cur.fetchone()

    def find_by_id(self, id):
        sql = f"select * from card where id={id}"
        self.cur.execute(sql)
        return self.cur.fetchone()

    def add_income(self, id, income):
        sql = f"update card set balance = balance + {income} where id = {id}"
        self.cur.execute(sql)
        self.conn.commit()
        print("Income was added!")

    def transfer_amount(self, from_card_num, to_card_num, amount):
        sql1 = f"update card set balance = balance - {amount} where number = {from_card_num}"
        self.cur.execute(sql1)

        sql2 = f"update card set balance = balance + {amount} where number = {to_card_num}"
        self.cur.execute(sql2)
        self.conn.commit()
        print("Success!")

    def delete_account(self, id):
        sql = f"delete from card where id = {id}"
        self.cur.execute(sql)
        self.conn.commit()
        print("The account has been closed!")

    def login(self):
        card_num = input("Enter your card number:")
        pin = input("Enter your PIN:")

        sql = f"select * from card where number={card_num} and pin={pin}"
        self.cur.execute(sql)
        result = self.cur.fetchone()

        if result is not None:
            print("You have successfully logged in!")
            my_account = result
            while True:
                self.print_menu2()
                user_input = input()
                if user_input == '1':
                    print(f"Balance: {self.find_by_id(my_account[0])[3]}")
                elif user_input == '2':
                    self.add_income(my_account[0], int(input("Enter income:")))
                elif user_input == '3':
                    print("Transfer")
                    card_num = input("Enter card number:")
                    verify_card_num = luhn_algorithm(card_num[0:-1])

                    if verify_card_num != int(card_num[-1]):
                        print("Probably you made a mistake in the card number. Please try again!")
                        continue

                    if self.find_by_card_num(card_num) is None:
                        print("Such a card does not exist.")
                        continue

                    if card_num == my_account[1]:
                        print("You can't transfer money to the same account!")
                        continue

                    amount = int(input("Enter how much money you want to transfer:"))

                    if amount > self.find_by_id(my_account[0])[3]:
                        print("Not enough money!")
                    else:
                        self.transfer_amount(my_account[1], card_num, amount)
                elif user_input == "4":
                    self.delete_account(my_account[0])
                    break
                elif user_input == "0":
                    return "exit"
        else:
            print("Wrong card number or PIN!")

    def run(self):
        while True:
            self.print_menu1()
            user_input = input("")
            if user_input == "1":
                self.create_account()
            elif user_input == "2":
                r = self.login()
                if r == 'exit':
                    break
            elif user_input == '0':
                print("Bye!")
                break


bank = SimpleBank()
bank.run()
