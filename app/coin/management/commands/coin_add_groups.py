from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from user_core.models import CustomGroup as Group


class Command(BaseCommand):
    help = 'Create default groups with permissions'

    def handle(self, *args, **kwargs):
        groups_and_permissions = {
            'coin_admin': [
                'view_gift',
                'add_gift',
                'change_gift',
                'delete_gift',
                'view_wallet',
                'view_event',
                'change_event',
                'delete_event',
                'add_event',
                'view_transaction',
                'change_transaction',
                'delete_transaction',
                'add_transaction',
            ],
            'coin_user': [
                'view_wallet',
                'view_gift',
                'view_event',
                'view_transaction',
                'add_transaction',
            ],
        }

        for group_name, permissions in groups_and_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Created group '{group_name}'")
            else:
                self.stdout.write(f"Group '{group_name}' already exists")

            for codename in permissions:
                try:
                    permission = Permission.objects.get(codename=codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        f"Permission '{codename}' does not exist")

        self.stdout.write(self.style.SUCCESS(
            'Default groups and permissions set up successfully.'))
