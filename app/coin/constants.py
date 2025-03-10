from django.utils.translation import gettext_lazy as _


class EventType:
    INCREASE = 'increase'
    DECREASE = 'decrease'
    EXCHANGE = 'exchange'
    TRANSFER = 'transfer'
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'

    CHOICES = [
        (INCREASE, _('Reward')),
        (DECREASE, _('Penalty')),
        (EXCHANGE, _('Exchange gift')),
        (TRANSFER, _('Transfer')),
        (DEPOSIT, _('Deposit coin')),
        (WITHDRAW, _('Withdraw coin')),
    ]


class TransactionStatus:
    STATUS_PENDING = 'pending'
    STATUS_SUCCESS = 'success'
    STATUS_FAIL = 'fail'

    CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_SUCCESS, _('Success')),
        (STATUS_FAIL, _('Fail')),
    ]


class Permission:
    # Transaction
    CAN_CHANGE_TRANSACTION_STATUS = 'change_transaction_status'
    CAN_CHANGE_OWN_TRANSACTION = 'change_own_transaction'

    # Wallet
    CAN_CHANGE_WALLET_BALANCE = 'change_wallet_balance'


COIN_USER = 'coin_user'
COIN_ADMIN = 'coin_admin'
