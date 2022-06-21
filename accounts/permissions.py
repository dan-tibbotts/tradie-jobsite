#################################################
# HOW TO USE THE PERMISSION MODULE IN TEST_FUNC #
#################################################

# 1. IMPORT THE MODULE
# from accounts.permissions import Permissions

# 2. ADD A USER_FIELD ATTRIBUTE IN TEST_FUNC
# user_field = self.get_object().staff_id  

# Note: 
# The user fields represents the field in the model to check against
# staff_id = represents the model field to check if the user is restricted to their own records
# if not checking a user field set user_field to None


# 2. RETURN THE FUNCTION IN THE TEST_FUNC METHOD LISTING ALL ALLOWED GROUPS
# e.g. 
# return Permissions(self.request).allow(user_field, 'Office Staff', '*Trade Staff', '*Supervisor')
#
# Note: adding an asterik (*) indicates the user only perform actions on their own record or if added to the record group


class Permissions():
    logged_user = None

    def __init__(self, request):
        self.logged_user = request.user


    def allow(self, user_field, *args, **kwargs):
        for arg in args:
            # Superuser or 'All' always has access
            if self.logged_user.is_superuser or arg == 'All':
                return True

            # if current user is in accepted group allow access
            if self.logged_user.groups.filter(name = arg).exists():
                return True
            else:
                if '*' in arg: # selected user can access own records only
                    try:
                        # loop through assigned users
                        for user in user_field.all():
                            # user is in the list, allow access
                            if user == self.logged_user:
                                return True
                    except:
                        # user_field is not iterable
                        # check if user attribute is current user
                        if str(user_field) == str(self.logged_user):
                            return True
        # deny access
        return False