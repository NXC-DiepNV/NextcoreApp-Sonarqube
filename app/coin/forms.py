from django import forms
from coin.constants import EventType, Permission
from coin.models import Event, Transaction

from .constants import (
    COIN_ADMIN,
    COIN_USER,
)

from unfold.widgets import UnfoldAdminSelectWidget


class CustomRelatedFieldWidgetWrapper(UnfoldAdminSelectWidget):

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        """
        Copy from parent, just change logic for attrs
        """
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        option_attrs = (
            # My Change logic to assign data-event-id to html
            {'data-type-id': value.instance.type}
        )
        if selected:
            option_attrs.update(self.checked_attribute)
        if "id" in option_attrs:
            option_attrs["id"] = self.id_for_label(option_attrs["id"], index)
        return {
            "name": name,
            "value": value,
            "label": label,
            "selected": selected,
            "index": index,
            "attrs": option_attrs,
            "type": self.input_type,
            "template_name": self.option_template_name,
            "wrap_label": True,
        }


class TransactionForm(forms.ModelForm):
    user_type = forms.CharField(
        widget=forms.HiddenInput(), required=False)
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        empty_label=None,
        required=False,
        widget=CustomRelatedFieldWidgetWrapper()
    )

    class Meta:
        model = Transaction
        fields = (
            'type',
            'event',
            'gift',
            'from_user',
            'to_user',
            'coin',
            'fee',
            'description',
            'status',
            'user_type',
        )

    class Media:
        js = (
            'js/jquery-3.7.1.min.js',
            'js/event_filter.js',
        )
        css = {'all': ('css/coin_styles.css',)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Form change
        if self.instance and self.instance.pk:
            return
        self.fields['user_type'].initial = COIN_ADMIN

        if self.user.is_superuser:
            return

        # Coin admin
        if self.user.has_perm(Permission.CAN_CHANGE_TRANSACTION_STATUS):
            return

        # Coin user
        self.fields['user_type'].initial = COIN_USER
        self.fields['type'].choices = [choice for choice in self.fields['type'].choices if choice[0] not in [
            EventType.DEPOSIT, EventType.WITHDRAW]]
        self.fields['fee'].widget.attrs['readonly'] = True
        self.fields['status'].widget.attrs['disabled'] = 'disabled'
        self.fields['status'].required = False  # Remove validate in front
        self.fields['from_user'].choices = [
            choice for choice in self.fields['from_user'].choices if choice[1] == str(self.user)
        ]
