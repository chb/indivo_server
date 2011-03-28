from base import Principal
# Principal object for requests made without
# a true principal. This class doesn't
# have any permissions outside of 
# the defaults it inhereits from the Principal
# class (i.e.) 'basicPrincipalRole', so it is basically
# an empty class
class NoUser(Principal):
    pass
