from .apps import MusifetchConfig


def is_in_group_contributor(user):
    return user.groups.filter(name='contributor').exists() or user.is_superuser
