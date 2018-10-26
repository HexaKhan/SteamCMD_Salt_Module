import logging
log = logging.getLogger(__name__)

__virtualname__ = 'steamcmd'

default_user = 'steam'
default_dir = '/home/{0}/Steam/'.format(default_user)
default_files = ['steamcmd.sh',
                 'linux32/steamcmd',
                 'linux32/crashhandler.so',
                 'linux32/libstdc++.so.6',
                 'linux32/steamcmd',
                 'linux32/steamerrorreporter']

def __virtual__():
  return __virtualname__

def install(directory=default_dir,
            user=default_user):

  directory = _path_format(directory)

  if __salt__['file.directory_exists'](directory):
    fileURL = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz'
    command = 'curl -sqL {0} | tar zxvf - -C {1}'.format(fileURL, directory)
    ret = __salt__['cmd.run'](command, runas=user, python_shell=True)
    return is_installed(directory)

  else:
    log.error('Directory {0} does not exist'.format(directory))
    return False

def is_installed(directory=default_dir):
  directory = _path_format(directory)

  for filename in default_files:
    if not __salt__['file.file_exists'](directory + filename):
      log.error('{0}{1} does not exist'.format(directory, filename))
      return False

  return True
    

def _path_format(directory_path):
  if directory_path[-1] == '/':
    return directory_path
  else:
    return directory_path + '/'
