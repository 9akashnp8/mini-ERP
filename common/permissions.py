from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    LoginRequiredMixin
)
from django.core.exceptions import PermissionDenied

class AllowedGroupsMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/login/'

    allowed_groups = []
    def test_func(self):
        user = self.request.user
        print(user.groups.all())
        if user.groups.filter(name__in=self.allowed_groups).exists():
            return True
        raise PermissionDenied("You do not have permission to access this page.")