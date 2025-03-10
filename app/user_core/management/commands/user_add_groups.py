from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from user_core.models import CustomGroup as Group


class Command(BaseCommand):
    help = 'Create default user_core groups with permissions'

    def handle(self, *args, **kwargs):
        all_permissions = Permission.objects.all()
        permission_codenames = [
            permission.codename for permission in all_permissions]
        groups_and_permissions = {
            'user_boss': permission_codenames,  # user_boss has all permission
            'user_member': [
                'view_customgroup',
                'view_customuser',
                'change_own_info',
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
