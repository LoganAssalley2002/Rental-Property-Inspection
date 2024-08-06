from django import template


register = template.Library() 


@register.filter
def has_group(user, group_name):
    '''
    Returns True if user belongs to group_name, False otherwise
    '''
    return user.groups.filter(name=group_name).exists()
