from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from django.utils import timezone

def create_log_entry(user, content_type, object_id, object_repr, action_flag, change_message, action_time=None):
    """
    Creates a log entry manually using LogEntry.objects.create().

    Args:
        user: The user who performed the action.
        content_type: The type of the model that was acted upon (ContentType instance).
        object_id: The primary key of the object involved.
        object_repr: A string representation of the object.
        action_flag: The type of action (1 for ADDITION, 2 for CHANGE, 3 for DELETION).
        change_message: A description of the change made.
        action_time: Optional. The timestamp of the action. Defaults to the current time.
    """
    if action_time is None:
        action_time = timezone.now()

    LogEntry.objects.create(
        user=user,
        content_type=content_type,
        object_id=str(object_id),  # Ensure object_id is stored as a string
        object_repr=object_repr,
        action_flag=action_flag,
        change_message=change_message,
        action_time=action_time
    )



"""
# Use case 
from packages.log_entry import create_log_entry
from django.contrib.contenttypes.models import ContentType

create_log_entry(
    user=request.user, --> when user is not defined and request is in function args or self.request.user --> when user is not defined and self is in function args or user --> when user is defined
    content_type=ContentType.objects.get_for_model(User),
    object_id=user.pk,
    object_repr=str(user),
    action_flag=1,
    change_message="Account created for user"
)

"""

