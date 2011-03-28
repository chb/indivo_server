import os
import string
import random
import upholstery
import datetime

USER = 'szabak'

def run():
  host = 'indivo.genepartnership.org'
  #host = 'indivo-staging.informedcohort.org'
  #host = 'indivobig.genepartnership.org'
  #host = 'x-staging.indivo.org'
  code_dirs = ['indivo_server', 'indivo_ui_server']
  deploy_obj = Deploy(host)
  #deploy_obj.init()
  deploy_obj.set_user(USER)
  deploy_obj.deploy(code_dirs)

class Deploy:

  def __init__(self, host):
    self.host = host
    self.users = ['steve', 'web']
    self.packages = [ 'apache2-mpm-prefork', 
                      'libapache2-mod-wsgi', 
                      'libapache2-mod-gnutls', 
                      'python2.6', 
                      'python-libxml2', 
                      'python-libxslt1', 
                      'python-psycopg2',
                      'python-django',
                      'postgresql-8.4']
  
    self.apt_get    = 'apt-get -y -qq '
    self.cd         = 'cd '
    self.chmod      = 'chmod '
    self.chown      = 'chown '
    self.echo       = 'echo '
    self.groupadd   = 'groupadd '
    self.groupdel   = 'groupdel '
    self.mkdir      = 'mkdir '
    self.mv         = 'mv '
    self.rm         = 'rm '
    self.sudo       = 'sudo -u '
    self.symlink    = 'ln -s '
    self.tar        = 'tar '
    self.touch      = 'touch '
    self.useradd    = 'useradd -m '

    self.tar_compress_flags   = 'czf'
    self.tar_decompress_flags = 'zxf'

    self.default_home_dir = '/home/'
    self.default_ssh_dir = '.ssh/'

    self.remote_sudoer_location = '/etc/sudoers'

  def get_host(self, username=''):
    if not username:
      return self.host
    else:
      return username + '@' + self.host

  def init(self):
    # test /tmp/successful
    create_users      = True
    install_packages  = True
    start_httpd       = True

    # SZ: First user gets sudo access
    if create_users and self.create_users(self.users):
      self.set_user(self.users[0])
      if install_packages and self.install_packages():
        start_httpd and self.start_httpd()

  def deploy(self, code_dirs):
    deploy_code = True
    if deploy_code:
      self.deploy(code_dirs)

  def create_users(self, users):
    authorized_keys_file = 'authorized_keys'
    public_key_location = self.get_public_key_location()
    sudo_group = self.add_sudo_group()

    for user in users:
      if users[0] == user:
        upholstery.run(self.useradd + user + ' -G ' + sudo_group)
      else:
        upholstery.run(self.useradd + user)

      # If a public key exists then push it to the server
      if public_key_location:
        upholstery.run(self.mkdir + self.default_home_dir + user + '/' + self.default_ssh_dir)
        upholstery.put(public_key_location, self.default_home_dir +  user + '/' + \
                                                        self.default_ssh_dir + \
                                                        authorized_keys_file)
      # Symlink all users > 0
      upholstery.run(self.symlink + self.default_home_dir + user + ' /' + user)
    self.change_mode(440, self.remote_sudoer_location)
    return True

  def add_sudo_group(self):
    sudo_group = self.random_string(6)
    self.set_user('root')
    self.add_group(sudo_group)
    self.change_mode(640, self.remote_sudoer_location)
    sudo_line = '%%' + sudo_group + ' ALL=(ALL) NOPASSWD:ALL' 
    upholstery.run(self.echo + '\'' + sudo_line + "' >> " + self.remote_sudoer_location)
    return sudo_group

  #def random_string(self, length, choices=[string.letters]):
  def random_string(self, length, choices=[]):
    if not choices:
      choices = [string.letters]
    return "".join([random.choice(''.join(choices)) for i in xrange(length)])

  def get_public_key_location(self):
    _possible_ssh_pubkey_locations = ['id_dsa.pub', 'id_dsa', 'id_rsa.pub', 'id_rsa']
    if os.environ.has_key('USER'):
      current_user = os.environ['USER']
    if os.path.exists(self.default_home_dir + current_user + '/' + self.default_ssh_dir):
      ssh_base_dir = self.default_home_dir + current_user + '/' + self.default_ssh_dir
      for default_ssh_pubkey_location in _possible_ssh_pubkey_locations:
        if os.path.exists(ssh_base_dir + default_ssh_pubkey_location):
          return ssh_base_dir + default_ssh_pubkey_location
    return False

  def set_user(self, user):
    upholstery.set(fab_hosts=[self.get_host(user)])

  def add_group(self, group, num_tries=0):
    try:
      upholstery.run(self.groupadd + group)
    except:
      if num_tries == 0:
        self.del_group(group)
        self.add_group(group, 1)
      else:
        pass
        #raise UpErr

  def del_group(self, group):
    upholstery.run(self.groupdel + group)

  def start_httpd(self):
    self.deploy_virtual_host()
    self.deploy_ports_conf()
    self.service('apache2', 'restart')
    self.service('postgresql-8.4', 'restart')
    return True

  def service(self, program, action):
    upholstery.sudo('service ' + program + ' ' + action)

  def install_packages(self):
    if  self._pre_install_packages() and \
        self._install_packages() and \
        self._post_install_packages():
      return True
    return False

  def _pre_install_packages(self):
    return True

  def _install_packages(self):
    if hasattr(self, 'packages'):
      for package in self.packages:
        upholstery.sudo(self.apt_get + ' install ' + package)
      return True
    return False

  def _post_install_packages(self):
    self.create_postgres_user('root')
    self.create_postgres_user('web')
    self.create_postgres_user('www-data')
    upholstery.run(self.sudo + 'postgres createdb indivo')
    return True

  def create_postgres_user(self, user):
    # SZ: All postgres users should NOT be superusers!
    upholstery.run(self.sudo + 'postgres createuser -s ' + user)

  def deploy_virtual_host(self):
    # SZ: randomize
    filename_virtual_host = 'virtual_host'
    virtual_host_path = '/etc/apache2/sites-enabled/000-default'
    if self.create_file(filename_virtual_host, virtual_host):
      upholstery.put(filename_virtual_host, filename_virtual_host)
      upholstery.local(self.rm + filename_virtual_host)
      upholstery.sudo(self.mv + filename_virtual_host + ' ' + virtual_host_path)
  
  def deploy_ports_conf(self):
    ports_conf= """
    NameVirtualHost *:80
    Listen 80
    Listen 8000
    """

    ports_path = '/etc/apache2/ports.conf'
    filename_ports_conf = 'ports_conf'
    if self.create_file(filename_ports_conf, ports_conf):
      upholstery.put(filename_ports_conf, filename_ports_conf)
      upholstery.local(self.rm + filename_ports_conf)
      upholstery.sudo(self.mv + filename_ports_conf + ' ' + ports_path)

  def create_file(self, filename, content, mode='w'):
    try:
      f = open(filename, mode)
      f.write(content)
      f.close()
    except:
      return False
    return True

  def change_mode(self, mode, file):
    if isinstance(mode, int):
      try:
        mode = str(mode)
      except:
        raise TypeError
    if isinstance(mode, str):
      upholstery.run(self.chmod + mode + ' ' + file)
      return True
    return False

  def deploy(self, code_dirs):
    self.datetime = datetime.datetime.today()
    if  self._pre_deploy()  and \
        self._deploy(code_dirs)      and \
        self._post_deploy():
      return True
    else:
      return False

  def _pre_deploy(self):
    return True
  
  def _deploy(self, code_dirs):
    compressed_file_name = 'tmp.tar.gz'
    exclude_dir = '.git'

    for code_dir in code_dirs:
      if os.path.exists(code_dir):
        upholstery.local(self.tar + ' ' + self.tar_compress_flags + ' ' + compressed_file_name + \
                         ' ' + code_dir + ' --exclude "' + exclude_dir + '"')
        upholstery.put(compressed_file_name, compressed_file_name)
        upholstery.local(self.rm + compressed_file_name)

        # Decompress and Clean up
        upholstery.run(self.tar + ' ' + self.tar_decompress_flags + ' ' + compressed_file_name)
        upholstery.run(self.rm + compressed_file_name)

        if self.datetime:
          indivo_servers_location = '/web/' + code_dir + 's/' + \
                                    code_dir + '-' + \
                                    str(self.datetime.year) + '_' + \
                                    str(self.datetime.month) + '_' + \
                                    str(self.datetime.day)
        else:
          indivo_server_location = '/web/'

        # SZ: Remove this in the future
        upholstery.sudo(self.mv + code_dir + ' ' + indivo_servers_location)

    return True

  def _post_deploy(self):
    self.set_user(USER)
    upholstery.sudo(self.chown + 'web:www-data -R /web/indivo_servers/')
    upholstery.sudo(self.chown + 'web:www-data -R /web/indivo_ui_servers/')
    #self.set_user('web')
    #upholstery.run(self.cd + '/web/indivo_server && ./reset.sh')

    # Restart apache
    upholstery.run(self.touch + '/tmp/successful')

    # SZ: For development
    #upholstery.run('python manage.py runserver 0.0.0.0:8000')

    return True

virtual_host = """
<VirtualHost *:8000>
 ServerAdmin steve.zabak@childrens.harvard.edu
 ServerName x-staging.indivo.org
 DocumentRoot /web/indivo_server
 Alias /static/ /web/indivo_server/static/
 EnableMMAP On
 EnableSendfile On
 LogLevel warn
 <Directory /web/indivo_server>
  Order deny,allow
  Allow from all
 </Directory>
 #RedirectMatch ^/$ https://localhost
 WSGIDaemonProcess indivo user=www-data group=www-data processes=1 maximum-requests=500 threads=10
 WSGIProcessGroup indivo
 WSGIScriptAlias / /web/indivo_server/django.wsgi
 WSGIPassAuthorization On
</VirtualHost>
<VirtualHost *:80>
 ServerAdmin steve.zabak@childrens.harvard.edu
 ServerName x-staging.indivo.org
 DocumentRoot /web/indivo_ui_server
 Alias /static/ /web/indivo_ui_server/ui/static/
 EnableMMAP On
 EnableSendfile On
 LogLevel warn
 <Directory /web/indivo_ui_server>
  Order deny,allow
  Allow from all
 </Directory>
 #RedirectMatch ^/$ https://localhost
 WSGIDaemonProcess indivo_ui user=www-data group=www-data processes=1 maximum-requests=500 threads=10
 WSGIProcessGroup indivo_ui
 WSGIScriptAlias / /web/indivo_ui_server/django.wsgi
 WSGIPassAuthorization On
</VirtualHost>
"""

if __name__ == '__main__':
  upholstery.main()
