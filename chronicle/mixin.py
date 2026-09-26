from django.shortcuts import redirect


class CustomLoginMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        return super(CustomLoginMixin,self).dispatch( request, *args, **kwargs)