# Convenience imports from pexpect
from __future__ import absolute_import
from pexpect import is_executable_file, EOF, TIMEOUT
import os

try:
    from pexpect import spawn as pty_spawn
    import pty
except ImportError:
    from pexpect.popen_spawn import PopenSpawn
    pty = None


def spawn(command, args=[], timeout=30, maxread=2000,
          searchwindowsize=None, logfile=None, cwd=None, env=None,
          ignore_sighup=True, echo=True, encoding='utf-8', **kwargs):
    codec_errors = kwargs.get('codec_errors', kwargs.get('errors', 'strict'))
    if pty is None:
        if args:
            command += ' ' + ' '.join(args)
        child = PopenSpawn(command, timeout=timeout, maxread=maxread,
                           searchwindowsize=searchwindowsize,
                           logfile=logfile, cwd=cwd, env=env,
                           encoding=encoding, codec_errors=codec_errors)
        child.echo = echo
    else:
        child = pty_spawn(command, args=args, timeout=timeout,
                          maxread=maxread, searchwindowsize=searchwindowsize,
                          logfile=logfile, cwd=cwd, env=env,
                          encoding=encoding, codec_errors=codec_errors)
    return child


# For backwards compatibility
spawnu = spawn


def which(filename):
    '''This takes a given filename; tries to find it in the environment path;
    then checks if it is executable. This returns the full path to the filename
    if found and executable. Otherwise this returns None.'''

    # Special case where filename contains an explicit path.
    if os.path.dirname(filename) != '' and is_executable_file(filename):
        return filename
    if 'PATH' not in os.environ or os.environ['PATH'] == '':
        p = os.defpath
    else:
        p = os.environ['PATH']
    pathlist = p.split(os.pathsep)
    for path in pathlist:
        ff = os.path.join(path, filename)
        if pty:
            if is_executable_file(ff):
                return ff
        else:
            pathext = os.environ.get('Pathext', '.exe;.com;.bat;.cmd')
            pathext = pathext.split(os.pathsep) + ['']
            for ext in pathext:
                if os.access(ff + ext, os.X_OK):
                    return ff + ext
    return None
