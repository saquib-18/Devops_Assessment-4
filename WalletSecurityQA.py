import unittest
import time
import sys

from DigitalWallet import DigitalWallet


class TestWalletSecurityQA(unittest.TestCase):

    def setUp(self):

        self.wallet = DigitalWallet(
            account_id="Wallet_A",
            initial_balance=2000.0,
            daily_limit=1500.0
        )

        self.target = DigitalWallet(
            account_id="Wallet_B",
            initial_balance=50.0
        )

    # -----------------------------------------
    # TEST 1: Normal Transaction
    # -----------------------------------------

    def test_01_normal_transaction(self):

        result = self.wallet.withdraw(200)

        self.assertEqual(result, "Success")

        self.assertEqual(
            self.wallet.verify_balance(),
            1800.0
        )

    # -----------------------------------------
    # TEST 2: Insufficient Balance
    # -----------------------------------------

    def test_02_insufficient_balance(self):

        result = self.wallet.withdraw(3000)

        self.assertEqual(
            result,
            "Failed: Insufficient balance"
        )

    # -----------------------------------------
    # TEST 3: Daily Limit
    # -----------------------------------------

    def test_03_daily_limit(self):

        self.wallet.withdraw(1200)

        result = self.wallet.withdraw(400)

        self.assertEqual(
            result,
            "Failed: Daily limit exceeded"
        )

    # -----------------------------------------
    # TEST 4: Multiple Failed PINs
    # -----------------------------------------

    def test_04_multiple_failed_pins(self):

        self.wallet.withdraw(
            10,
            pin_correct=False
        )

        self.wallet.withdraw(
            10,
            pin_correct=False
        )

        result = self.wallet.withdraw(
            10,
            pin_correct=False
        )

        self.assertIn(
            "Suspicious Transaction Flagged: Multiple failed PIN attempts",
            result
        )

    # -----------------------------------------
    # TEST 5: Suspicious Transaction
    # -----------------------------------------

    def test_05_suspicious_transaction(self):

        rich_wallet = DigitalWallet(
            account_id="Wallet_Rich",
            initial_balance=60000.0,
            daily_limit=60000.0
        )

        result = rich_wallet.withdraw(25000)

        self.assertIn(
            "Suspicious Transaction Flagged: Large transaction",
            result
        )

    # -----------------------------------------
    # TEST 6: Duplicate Transaction
    # -----------------------------------------

    def test_06_duplicate_transaction(self):

        self.wallet.transfer(
            self.target,
            150
        )

        result = self.wallet.transfer(
            self.target,
            150
        )

        self.assertIn(
            "Suspicious Transaction Flagged: Duplicate transaction",
            result
        )

    # -----------------------------------------
    # TEST 7: Negative Amount
    # -----------------------------------------

    def test_07_negative_amount(self):

        result = self.wallet.deposit(-100)

        self.assertIn(
            "Suspicious Transaction Flagged: Negative/Zero amount",
            result
        )

    # -----------------------------------------
    # TEST 8: Concurrent Transactions
    # -----------------------------------------

    def test_08_concurrent_transactions(self):

        for _ in range(5):
            self.wallet.deposit(10)

        result = self.wallet.withdraw(10)

        self.assertIn(
            "Suspicious Transaction Flagged: More than 5 transactions in 10 minutes",
            result
        )


# =============================================
# CUSTOM JENKINS TEST RESULT
# =============================================

class JenkinsPipelineTextResult(unittest.TextTestResult):

    def startTest(self, test):

        test_name = (
            test._testMethodName
            .split('_', 2)[-1]
            .replace('_', ' ')
            .capitalize()
        )

        self.stream.write(
            f" -> Verifying Step: {test_name:<30} "
        )

        self.stream.flush()

    def addSuccess(self, test):

        super().addSuccess(test)

        self.stream.writeln(
            "[ PASSED ]"
        )

    def addFailure(self, test, err):

        super().addFailure(test, err)

        self.stream.writeln(
            "[ FAILED ]"
        )


# =============================================
# MAIN QA EXECUTION
# =============================================

if __name__ == '__main__':

    print("=" * 60)

    print(
        " EXECUTING WALLET SECURITY QA PIPELINE STAGES "
    )

    print("=" * 60)

    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=JenkinsPipelineTextResult
    )

    suite = unittest.TestLoader().loadTestsFromTestCase(
        TestWalletSecurityQA
    )

    result = runner.run(suite)

    print("=" * 60)

    if result.wasSuccessful():

        print(
            "PIPELINE STATUS: ALL 8 SECURITY CHECKS PASSED SUCCESSFULLY"
        )

        sys.exit(0)

    else:

        print(
            "PIPELINE STATUS: FAILURE DETECTED IN TEST SUITE"
        )

        sys.exit(1)