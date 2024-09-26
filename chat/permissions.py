from rest_framework import permissions


class IsThreadParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(pk=request.user.id)


class IsAllowedMarkMessageRead(permissions.BasePermission):
    """
    Permission class to check if a user is allowed to mark a message as read.
    The user can only mark a message as read if they are a participant in the thread
    and the message does not belong to them.
    """
    def has_object_permission(self, request, view, obj):
        return (
                obj.thread.participants.filter(pk=request.user.id)
                and obj.user_id != request.user.id
        )
