import pytest

import stack.util
import subprocess

class TestUtil:
	def test_exec_wrapper(self):
		_exec = stack.util._exec

		# by default, we get stdout decoded as a string
		results = _exec('whoami')
		assert results.returncode == 0
		assert results.stdout.strip() == 'root'
		assert results.stderr == ''

		# but we can disable it
		results = _exec('whoami', stdout=None)
		assert results.returncode == 0
		assert results.stdout == None
		assert results.stderr == ''

		# we can disable the encoding
		results = _exec('whoami', encoding=None)
		assert results.returncode == 0
		assert results.stdout.strip() == b'root'
		assert results.stderr == b''

		# and we have stderr
		results = _exec(['whoami', '-???'])
		assert results.returncode != 0
		assert results.stdout == ''
		assert results.stderr != ''

		# and optional shlex-based string splitting
		results = _exec('whoami -???', shlexsplit=True)
		assert results.returncode != 0
		assert results.stdout == ''
		assert results.stderr != ''

		# we can use shell=True
		results = _exec('echo $USER', shell=True)
		assert results.returncode == 0
		assert results.stdout.strip() == 'root'
		assert results.stderr == ''

		# and shell features
		results = _exec('echo $USER | rev && date', shell=True)
		assert results.returncode == 0
		assert results.stdout.strip().startswith('toor')
		assert results.stderr == ''

		# we can pass in text to SDTIN
		results = _exec('cat', input='a string')
		assert results.returncode == 0
		assert results.stdout.strip() == 'a string'
		assert results.stderr == ''

		# and you can change directories
		results = _exec('echo $PWD', shell=True, cwd='/export')
		assert results.returncode == 0
		assert results.stdout.strip() == '/export'
		assert results.stderr == ''

		# or redirect stderr to stdout
		results = _exec('whoami -???', shlexsplit=True, stderr=subprocess.STDOUT)
		assert results.returncode != 0
		assert results.stdout.strip() != ''
		assert results.stderr == None

		# or redirect to /dev/null
		results = _exec('whoami -???', shlexsplit=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
		assert results.returncode != 0
		assert results.stdout == None
		assert results.stderr == None

		# unknown commands still error
		with pytest.raises(FileNotFoundError):
			_exec('whodis')


