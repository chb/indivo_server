"""
Accounts and authentication
"""

from base import *
from django.utils import simplejson
from indivo.lib import utils
import indivo

##
## Accounts
##
MAX_FAILED_LOGINS = 3
UNINITIALIZED, ACTIVE, DISABLED, RETIRED = 'uninitialized', 'active', 'disabled', 'retired'

# in seconds
if hasattr(settings, 'ACCOUNT_REENABLE_TIMEOUT'):
    ACCOUNT_REENABLE_TIMEOUT = settings.ACCOUNT_REENABLE_TIMEOUT
else:
    ACCOUNT_REENABLE_TIMEOUT = None

class Account(Principal):
    Meta = BaseMeta()
    
    account = models.OneToOneField(Principal, primary_key = True, parent_link = True)
    
    # secrets to create the account
    primary_secret = models.CharField(max_length=16, null=True)
    secondary_secret = models.CharField(max_length=8, null=True)
    
    # account's name and contact email
    full_name = models.CharField(max_length = 150, null= False)
    contact_email = models.CharField(max_length = 300, null = False)
    
    # password
    # password_hash = models.CharField(max_length = 64)
    # password_salt = models.CharField(max_length = 64)
    
    # login status
    last_login_at = models.DateTimeField(auto_now_add=False, null=True)
    last_failed_login_at = models.DateTimeField(auto_now_add=False, null=True)
    total_login_count = models.IntegerField(default=0)
    failed_login_count = models.IntegerField(default=0)
    
    STATES = ((UNINITIALIZED, u'Uninitialized (Needs Password)'),
              (ACTIVE, u'Active'),
              (DISABLED, u'Disabled / Locked'),
              (RETIRED, u'Retired'))
    
    # keep track of the state of the user
    state = models.CharField(max_length=50, choices=STATES, default=UNINITIALIZED)
    last_state_change = models.DateTimeField(auto_now_add=False, null=True)
    
    def __unicode__(self):
        return 'Account %s' % self.id

    @property
    def secondary_secret_pretty(self):
        if not self.secondary_secret:
            return 'None'
        else:
            return self.secondary_secret[:3] + '-' + self.secondary_secret[3:]

    def save(self, *args, **kwargs):
        """ Enforce case-insensitive emails. """
        self.email = self.email.lower().strip()
        super(Account,self).save(*args, **kwargs)
    
    # Accesscontrol:
    # roles that an Account could have
    def ownsRecord(self, record):
        """
        True if the Account is the owner of the record
        """
        try:
            return record.owner == self
        except:
            return False
    
    def fullySharesRecord(self, record):
        """
        True if the Account has a full share of the record
        """
        try:
            return indivo.models.AccountFullShare.objects.filter(record=record, with_account=self)
        except:
            return False
    
    def isInCarenet(self, carenet):
        """
        True if the Account is in the specified carenet. Note:
        Accounts may be in multiple carenets for multiple records
        """
        try:
            return indivo.models.CarenetAccount.objects.filter(carenet=carenet, account=self)
        except:
            return False
    
    def on_successful_login(self):
        self.last_login_at = datetime.now()
        self.total_login_count += 1
        self.failed_login_count = 0
        self.save()
    
    def on_failed_login(self):
        self.last_failed_login_at = datetime.utcnow()
        self.failed_login_count += 1
        if self.failed_login_count >= MAX_FAILED_LOGINS:
            self.set_state(DISABLED)
        self.save()
    
    def set_state(self, state):
        if self.state == RETIRED:
            raise Exception("account is retired, no further state changes allowed")
    
        self.state = state
        self.last_state_change = datetime.utcnow()
    
    def disable(self):
        self.set_state(DISABLED)
    
    @property
    def is_active(self):
        # if the account is disabled and we've waited long enough, reenable it
        # but only if the system is configured to allow for this reenablement
        # by default it is not
        if ACCOUNT_REENABLE_TIMEOUT and self.state == DISABLED and self.last_failed_login_at and \
            datetime.utcnow() - self.last_failed_login_at > timedelta(seconds=ACCOUNT_REENABLE_TIMEOUT):
            self.set_state(ACTIVE)
            self.failed_login_count = 0
            self.save()
        
        return self.state == ACTIVE
    
    def generate_secrets(self, secondary_secret_p = True):
        self.primary_secret = utils.random_string(16)
        if secondary_secret_p:
            self.secondary_secret = utils.random_string(6, [string.digits])
        else:
            self.secondary_secret = None
        self.save()
    
    # email the owner of the record with the secret
    def send_secret(self):
        # mail template
        subject = utils.render_template_raw('email/secret/subject', {'account': self}, type='txt').strip()
        body = utils.render_template_raw('email/secret/body',
                                            {'account': self,
                                          'url_prefix': settings.UI_SERVER_URL,
                                  'email_support_name': settings.EMAIL_SUPPORT_NAME,
                               'email_support_address': settings.EMAIL_SUPPORT_ADDRESS,
                                           'full_name': self.full_name or self.contact_email},
                                        type='txt')
        
        utils.send_mail(subject, body, 
                        "%s <%s>" % (settings.EMAIL_SUPPORT_NAME, settings.EMAIL_SUPPORT_ADDRESS), 
                        ["%s <%s>" % (self.full_name or self.contact_email, self.contact_email)])
    
    def notify_account_of_new_message(self):
        subject = utils.render_template_raw('email/new_message/subject', {'account': self}, type='txt').strip()
        body = utils.render_template_raw('email/new_message/body', 
                                            {'account': self, 
                                           'full_name': self.full_name or self.contact_email,
                                          'url_prefix': settings.SITE_URL_PREFIX, 
                                  'email_support_name': settings.EMAIL_SUPPORT_NAME,
                               'email_support_address': settings.EMAIL_SUPPORT_ADDRESS }, 
                                        type='txt')
        utils.send_mail(subject, body, 
                        "%s <%s>" % (settings.EMAIL_SUPPORT_NAME, settings.EMAIL_SUPPORT_ADDRESS), 
                        ["%s <%s>" % (self.full_name or self.contact_email, self.contact_email)])
    
    def send_welcome_email(self):
        subject = utils.render_template_raw('email/welcome/subject', {'account': self}, type='txt').strip()
        body = utils.render_template_raw('email/welcome/body', 
                                            { 'account': self, 
                                            'full_name': self.full_name or self.contact_email,
                                           'url_prefix': settings.UI_SERVER_URL, 
                                   'email_support_name': settings.EMAIL_SUPPORT_NAME,
                                'email_support_address': settings.EMAIL_SUPPORT_ADDRESS }, 
                                        type='txt')
        utils.send_mail(subject, body, 
                        "%s <%s>" % (settings.EMAIL_SUPPORT_NAME, settings.EMAIL_SUPPORT_ADDRESS), 
                        ["%s <%s>" % (self.full_name or self.contact_email, self.contact_email)])
    
    ##
    ## password stuff. This used to be stored in this table, but now it's stored
    ## in the accountauthsystems
    ##
    @property
    def password_info(self):
        try:
            return self.auth_systems.get(auth_system=AuthSystem.PASSWORD())
        except AccountAuthSystem.DoesNotExist:
            return None
        except AccountAuthSystem.MultipleObjectsReturned:
            # Added a database constraint: this should never happen
            raise
    
    def _add_password_auth_system(self, username):
        self.auth_systems.get_or_create(auth_system=AuthSystem.PASSWORD(), username=username.lower().strip())
    
    def _password_params_get(self):
        if not self.password_info:
            return None
        return simplejson.loads(self.password_info.auth_parameters or 'null') or {}
    
    def _password_params_set(self, val):
        info = self.password_info
        if info:
            info.auth_parameters = simplejson.dumps(val)
            info.save()
    
    password_params = property(_password_params_get, _password_params_set)
    
    def _password_hash_get(self):
        if self.password_params:
            return self.password_params.get('password_hash', None)
        else:
            return None
    
    def _password_hash_set(self, value):
        new_params = self.password_params
        new_params['password_hash'] = value
        self.password_params = new_params
    
    password_hash = property(_password_hash_get, _password_hash_set)
    
    def _password_salt_get(self):
        return self.password_params.get('password_salt', None)
    
    def _password_salt_set(self, value):
        new_params = self.password_params
        new_params['password_salt'] = value
        self.password_params = new_params
    
    password_salt = property(_password_salt_get, _password_salt_set)
    
    def set_username(self, username):
        """
        set the username
        """
        try:
            auth_system = self.auth_systems.get(auth_system=AuthSystem.PASSWORD())
        except AccountAuthSystem.DoesNotExist:
            raise Exception("need to initialize the password auth system before trying to set the username")
    
        auth_system.username = username
        auth_system.save()
    
    def set_username_and_password(self, username, password=None):
        """Setup the username and password.
        
        password can be null if we don't want to set one yet.
        """
        self._add_password_auth_system(username)
        if password:
            self.password = password
        self.save()
    
    def reset(self):
        self.state = UNINITIALIZED
        self.generate_secrets()
        self.save()
    
    def send_forgot_password_email(self):
        subject = utils.render_template_raw('email/forgot_password/subject', {'account': self}, type='txt').strip()
        body = utils.render_template_raw('email/forgot_password/body', 
                                            {'account': self, 
                                          'url_prefix': settings.UI_SERVER_URL,
                                  'email_support_name': settings.EMAIL_SUPPORT_NAME, 
                               'email_support_address': settings.EMAIL_SUPPORT_ADDRESS},
                                            type='txt')
        utils.send_mail(subject, body, 
                        "%s <%s>" % (settings.EMAIL_SUPPORT_NAME, settings.EMAIL_SUPPORT_ADDRESS), 
                        ["%s <%s>" % (self.full_name or self.contact_email, self.contact_email)])
    
    @classmethod
    def compute_hash(cls, password, salt):
        if not (isinstance(password, str) and isinstance(salt, str)):
            try:
                salt = str(salt)
                password = str(password)
            except:
                raise Exception('Password and Salt need to be strings')
        m = hashlib.sha256()
        m.update(salt)
        m.update(password)
        return m.hexdigest()
    
    def password_get(self):
        raise Exception('you cannot read the password')
    
    def password_set(self, new_password):
        # generate a new salt
        self.password_salt = utils.random_string(20)
        
        # compute the hash
        self.password_hash = self.compute_hash(new_password, self.password_salt)
        if self.state == UNINITIALIZED:
            self.set_state(ACTIVE)
    
    def password_check(self, password_try):
        return self.password_hash == self.compute_hash(password_try, self.password_salt)
    
    @property
    def default_record(self):
        return self.records_owned_by.all()[0]
    
    @property
    def records_administered(self):
        return self.records_owned_by
    
    password = property(password_get, password_set)

class AuthSystem(Object):
    short_name = models.CharField(max_length=100, unique=True)
    
    # is this authentication system handled internally by Indivo X?
    # otherwise externally by the Chrome App
    internal_p = models.BooleanField(default=False)
    
    @classmethod
    def PASSWORD(cls):
        # FIXME: memoize this
        return cls.objects.get_or_create(short_name='password', internal_p=True)[0]

class AccountAuthSystem(Object):
    account         = models.ForeignKey(Account, related_name = 'auth_systems')
    auth_system = models.ForeignKey(AuthSystem)
    
    username = models.CharField(max_length = 250)
    
    # json content for extra parameters
    auth_parameters = models.CharField(max_length = 2000, null = True)
    user_attributes = models.CharField(max_length = 2000, null = True)
    
    class Meta:
        app_label = INDIVO_APP_LABEL
        
        # One account can't have duplicate auth_systems
        # One auth_system can't have duplicate usernames
        unique_together = (('auth_system', 'account'),
                            ('auth_system', 'username'),
                          )

    def save(self, *args, **kwargs):
        """ Enforce lowercase usernames. """
        self.username = self.username.lower().strip()
        super(AccountAuthSystem,self).save(*args, **kwargs)
