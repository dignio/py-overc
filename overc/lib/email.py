import os
import shlex
import subprocess
import logging

logger = logging.getLogger(__name__)


class EmailPlugin(object):
    """ Email plugin """

    def __init__(self, name, cwd, command):
        self.name = name
        self.cwd = cwd
        self.command_str = command
        self.command = shlex.split(self.command_str)

    def send(self, message):
        """ Send a message
        :param message: Message
        :type message: unicode
        :exception OSError: plugin not found
        :exception subprocess.CalledProcessError: plugin execution error (non-zero return code)
        """
        # Execute
        process = subprocess.Popen(
            self.command,
            cwd=self.cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        try:
            # Run
            process.stdin.write(message)
            process.stdin.close()

            # Wait, analyze retcode
            process.wait()

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, self.command_str, '')
        finally:
            process.stdout.close()
