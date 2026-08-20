import time


class DigitalWallet:

    def __init__(self, account_id, initial_balance=0.0, daily_limit=5000.0):
        self.account_id = account_id
        self.balance = initial_balance
        self.daily_limit = daily_limit
        self.today_transacted = 0.0
        self.transactions = []
        self.failed_pin_attempts = 0

    def deposit(self, amount):

        if amount <= 0:
            return self._flag_suspicious(
                "Deposit",
                amount,
                "Negative/Zero amount"
            )

        self.balance += amount

        self.transactions.append(
            (time.time(), "Deposit", amount, "Normal")
        )

        return "Success"

    def withdraw(self, amount, pin_correct=True):

        if not pin_correct:

            self.failed_pin_attempts += 1

            if self.failed_pin_attempts >= 3:
                return self._flag_suspicious(
                    "Withdrawal",
                    amount,
                    "Multiple failed PIN attempts"
                )

            return "Failed: Invalid PIN"

        self.failed_pin_attempts = 0

        if amount <= 0:
            return self._flag_suspicious(
                "Withdrawal",
                amount,
                "Negative amount"
            )

        if amount > self.balance:
            return "Failed: Insufficient balance"

        if self.today_transacted + amount > self.daily_limit:
            return "Failed: Daily limit exceeded"

        if amount > 10000:
            return self._flag_suspicious(
                "Withdrawal",
                amount,
                "Large transaction"
            )

        if amount == 999.99 or amount == 444.44:
            return self._flag_suspicious(
                "Withdrawal",
                amount,
                "Unusual transaction amount"
            )

        if self._check_frequency_rule():
            return self._flag_suspicious(
                "Withdrawal",
                amount,
                "More than 5 transactions in 10 minutes"
            )

        self.balance -= amount
        self.today_transacted += amount

        self.transactions.append(
            (time.time(), "Withdrawal", amount, "Normal")
        )

        return "Success"

    def transfer(self, target_account, amount):

        if amount <= 0:
            return self._flag_suspicious(
                "Transfer",
                amount,
                "Negative amount"
            )

        if amount > self.balance:
            return "Failed: Insufficient balance"

        now = time.time()

        for t, t_type, t_amt, status in self.transactions[-3:]:

            if (
                t_type == "Transfer"
                and t_amt == amount
                and (now - t) < 10
            ):
                return self._flag_suspicious(
                    "Transfer",
                    amount,
                    "Duplicate transaction"
                )

        self.balance -= amount
        target_account.deposit(amount)

        self.transactions.append(
            (now, "Transfer", amount, "Normal")
        )

        return "Success"

    def get_history(self):
        return self.transactions

    def get_daily_limit(self):
        return self.daily_limit

    def verify_balance(self):
        return self.balance

    def _flag_suspicious(self, transaction_type, amount, reason):

        flagged_status = (
            f"Suspicious Transaction Flagged: {reason}"
        )

        self.transactions.append(
            (time.time(), transaction_type, amount, flagged_status)
        )

        return flagged_status

    def _check_frequency_rule(self):

        now = time.time()

        recent_transactions = [
            t for t in self.transactions
            if (now - t[0]) < 600
        ]

        return len(recent_transactions) >= 5