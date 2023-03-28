from django.forms import (
    ModelForm,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
    CharField
)
from django.contrib.auth.models import User, Group

class UserForm(ModelForm):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    groups = ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        widget=CheckboxSelectMultiple,
        required=True
    )

    class Meta:

        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "groups"
        ]
        
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # override the available group options to
        # only groups that logged in user is part of
        groups_field = self.fields.get("groups")
        groups_field.queryset = user.groups.all()



