import ast

from django import forms
from django.contrib.admin import widgets

from notification.models import NotificationGroup, Notification, Template, NotificationContext


class NotificationGroupForm(forms.ModelForm):

    title = forms.CharField()
    users_ids_to_group = forms.Field(initial=[])

    class Meta:
        model = NotificationGroup
        fields = ('title', 'notification_type',)

    def save_m2m(self):
        """Must be."""
        return

    def clean(self):
        super().clean()

        try:
            users_ids = ast.literal_eval(self.cleaned_data.get('users_ids_to_group'))
            if not users_ids:
                raise forms.ValidationError(
                    "Users ids are required."
                )
        except Exception as exc:
            raise forms.ValidationError(
                "Please ensure about correct users_ids."
            ) from exc

    def save(self, commit=True):
        title = self.cleaned_data.get('title')
        notification_type = self.cleaned_data.get('notification_type')

        notification_group = NotificationGroup(
            title=title,
            notification_type=notification_type,
        )
        return notification_group


class NotificationForm(forms.ModelForm):

    notification_group = forms.ModelChoiceField(
        queryset=NotificationGroup.objects.all(),
        required=True,
    )
    template = forms.ModelChoiceField(
        queryset=Template.objects.all(),
        required=True,
    )

    send_date = forms.CharField(widget=widgets.AdminSplitDateTime)

    class Meta:
        model = Notification
        fields = ()

    def save_m2m(self):
        """Must be."""
        return

    def save(self, commit=True):
        notification_group = self.cleaned_data.get('notification_group')
        template = self.cleaned_data.get('template')
        send_date = " ".join(ast.literal_eval(self.cleaned_data.get('send_date')))
        context = NotificationContext(
            params={"group_id": notification_group.id},
            # теги в params
            template=template
        )
        context.save()

        notification = Notification(
            send_date=send_date,
            context=context,

        )
        return notification
