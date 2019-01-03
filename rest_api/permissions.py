from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class BuyerViewPermission(BasePermission):

    def has_permission(self, request: Request, view):
        try:
            return request.user.is_staff or request.user.id == request.parser_context['kwargs']['buyer']
        except KeyError:
            return False
