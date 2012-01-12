from base import Principal

class NoUser(Principal):

    """ Principal object for requests made without a true principal. 

    This class doesn't have any permissions outside of the defaults it 
    inhereits from the Principal class (i.e.) 'basicPrincipalRole', 
    so it is basically an empty class.

    """

    @classmethod
    def get_nouser(cls):
        return cls.objects.get_or_create(email='nouser@indivo.org')[0]

class AdminUser(Principal):
    """ Principal objects for users of the admin (no oauth credentials)."""
    
    def adminRole(self):
        return True
