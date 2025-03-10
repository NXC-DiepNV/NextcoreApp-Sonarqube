from django.core.management.base import BaseCommand
from coin.models import Wallet

from user_core.models import CustomUser as User


class Command(BaseCommand):
    help = "Add wallets for users who don't already have one"

    def handle(self, *args, **kwargs):
        users_without_wallets = User.objects.filter(
            coin_wallet__isnull=True)  # Lấy danh sách user chưa có wallet
        for user in users_without_wallets:
            Wallet.objects.create(user=user, balance=0)
            self.stdout.write(f"Created wallet for user: {user.username}")
        self.stdout.write("All wallets have been added.")
