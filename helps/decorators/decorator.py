from django.contrib.auth.models import User
from rest_framework.response import Response
from helps.common.generic import Generichelps as ghelp
from rest_framework import status


from functools import wraps


class CommonDecorator:

    def get_permission(users=[], message='Permission Denied!'):
        lower_case_users = [user.lower() for user in users]
        permissions = []
        def decorator(func):
            def wrapper_func(request, *args, **kwargs):
                ghelp().getPermissionsList(User=User, username=request.user.username, permissions=permissions, active=True)
                if permissions:
                    if any(permission in lower_case_users for permission in permissions):
                        return func(request, *args, **kwargs)
                    else:
                        return Response({'message': message}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'message': message}, status=status.HTTP_403_FORBIDDEN)
            return wraps(func)(wrapper_func)
        return decorator

    def allow_users(users=[], message1='Permission Denied!', message2='group is empty!'):
        lower_case_users = [user.lower() for user in users]
        def decorator(func):
            def wrapper_func(request, *args, **kwargs):
                if 'all' in lower_case_users:
                    return func(request, *args, **kwargs)
                else:
                    if request.user.groups.exists():
                        groups = [group.name.lower() for group in request.user.groups.all()]
                        if any(group in lower_case_users for group in groups):
                            return func(request, *args, **kwargs)
                        else:
                            return Response({'message': message1}, status=status.HTTP_403_FORBIDDEN)
                    else:
                        if request.user.is_superuser:
                            return func(request, *args, **kwargs)
                        else:
                            return Response({'message': message2}, status=status.HTTP_404_NOT_FOUND)
            return wraps(func)(wrapper_func)
        return decorator
    
    def allow_superuser(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_superuser:
                return Response({'message': 'Permission Denied!'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return view_func(request, *args, **kwargs)
        return wrapper_func
    
    # def param_decorator(*args, **kwargs):
    #     def inner(func):
    #         print("-------------------------------- ", kwargs)
    #         func()    
    #     return inner