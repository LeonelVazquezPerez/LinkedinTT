from Account import Account

class accountController:

    accounts = []

    def selectAccount(self):

        flag = 0

        with open('accounts.txt') as f:
            lines = f.readlines()

        for line in lines:
            data = line.split(" // ")
            a = Account(str(data[0]), str(data[1]))

            if len(self.accounts) == 0:
                self.accounts.append(a)
                print("Account selected: " + data[0])
                flag = 1
                break
            else:
                flagC = 0
                for account in self.accounts:
                    if a.username == account.username:
                        flagC = 1

                if flagC == 0:
                    self.accounts.append(a)
                    print("Account selected: " + data[0])
                    flag = 1
                    break

        if flag == 1:
            return a
        else:
            return Account("", "")

    def closeAccount(self, account):
        self.accounts.remove(account)
        print("Account removed: " + account.username)