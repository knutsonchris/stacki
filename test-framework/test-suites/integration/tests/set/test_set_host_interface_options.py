import json
from textwrap import dedent


class TestSetHostInterfaceOptions:
	def test_no_hosts(self, host):
		result = host.run('stack set host interface options')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "host" argument is required
			{host ...} {options=string} [interface=string] [mac=string] [network=string]
		''')

	def test_no_matching_hosts(self, host):
		result = host.run('stack set host interface options a:test')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "host" argument is required
			{host ...} {options=string} [interface=string] [mac=string] [network=string]
		''')

	def test_no_parameters(self, host):
		result = host.run('stack set host interface options frontend-0-0')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "options" parameter is required
			{host ...} {options=string} [interface=string] [mac=string] [network=string]
		''')

	def test_no_selector(self, host):
		result = host.run('stack set host interface options frontend-0-0 options=test')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "interface" or "mac" or "network" parameter is required
			{host ...} {options=string} [interface=string] [mac=string] [network=string]
		''')

	def test_invalid_interface(self, host):
		result = host.run('stack set host interface options frontend-0-0 interface=eth9 options=test')
		assert result.rc == 255
		assert result.stderr == 'error - interface "eth9" does not exist for host "frontend-0-0"\n'

	def test_invalid_mac(self, host):
		result = host.run('stack set host interface options frontend-0-0 mac=00:11:22:33:44:55 options=test')
		assert result.rc == 255
		assert result.stderr == 'error - mac "00:11:22:33:44:55" does not exist for host "frontend-0-0"\n'

	def test_invalid_network(self, host):
		result = host.run('stack set host interface options frontend-0-0 network=test options=test')
		assert result.rc == 255
		assert result.stderr == 'error - network "test" does not exist for host "frontend-0-0"\n'

	def test_invalid_combo(self, host, add_host, add_network):
		# Add an interface with an interface and network to our test host
		result = host.run('stack add host interface backend-0-0 interface=eth0 network=test')
		assert result.rc == 0

		# Add a second interface with an interface and a mac to our test host
		result = host.run('stack add host interface backend-0-0 interface=eth1 mac=00:11:22:33:44:55')
		assert result.rc == 0

		# Now try to set the data with a bad combo
		result = host.run(
			'stack set host interface options backend-0-0 network=test interface=eth1 options=test'
		)
		assert result.rc == 255
		assert result.stderr == 'error - combination of "eth1, test" does not exist for host "backend-0-0"\n'

	def test_by_network(self, host, add_host, add_network):
		# Add an interface with an interface and network to our test host
		result = host.run('stack add host interface backend-0-0 interface=eth0 network=test')
		assert result.rc == 0

		# Set the host interface options
		result = host.run('stack set host interface options backend-0-0 network=test options=test_options')
		assert result.rc == 0

		# Check that it made it into the database
		result = host.run('stack list host interface backend-0-0 output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [{
			'channel': None,
			'default': None,
			'host': 'backend-0-0',
			'interface': 'eth0',
			'ip': None,
			'mac': None,
			'module': None,
			'name': None,
			'network': 'test',
			'options': 'test_options',
			'vlan': None
		}]

	def test_by_interface(self, host, add_host_with_interface):
		# Set the host interface options
		result = host.run('stack set host interface options backend-0-0 interface=eth0 options=test_options')
		assert result.rc == 0

		# Check that it made it into the database
		result = host.run('stack list host interface backend-0-0 output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [{
			'channel': None,
			'default': None,
			'host': 'backend-0-0',
			'interface': 'eth0',
			'ip': None,
			'mac': None,
			'module': None,
			'name': None,
			'network': None,
			'options': 'test_options',
			'vlan': None
		}]

		# Now set the options back to NULL
		result = host.run('stack set host interface options backend-0-0 interface=eth0 options=null')
		assert result.rc == 0

		# Did it stick?
		result = host.run('stack list host interface backend-0-0 output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [{
			'channel': None,
			'default': None,
			'host': 'backend-0-0',
			'interface': 'eth0',
			'ip': None,
			'mac': None,
			'module': None,
			'name': None,
			'network': None,
			'options': None,
			'vlan': None
		}]

	def test_by_mac(self, host, add_host):
		# Add an interface with a mac to our test host
		result = host.run('stack add host interface backend-0-0 mac=00:11:22:33:44:55')
		assert result.rc == 0

		# Set the host interface options
		result = host.run('stack set host interface options backend-0-0 mac=00:11:22:33:44:55 options=test_options')
		assert result.rc == 0

		# Check that it made it into the database
		result = host.run('stack list host interface backend-0-0 output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [{
			'channel': None,
			'default': None,
			'host': 'backend-0-0',
			'interface': None,
			'ip': None,
			'mac': '00:11:22:33:44:55',
			'module': None,
			'name': None,
			'network': None,
			'options': 'test_options',
			'vlan': None
		}]

	def test_all_parameters(self, host, add_host, add_network):
		# Add an interface with an interface, mac, and network to our test host
		result = host.run(
			'stack add host interface backend-0-0 interface=eth0 '
			'mac=00:11:22:33:44:55 network=test'
		)
		assert result.rc == 0

		# Set the host interface options
		result = host.run(
			'stack set host interface options backend-0-0 interface=eth0 '
			'mac=00:11:22:33:44:55 network=test options=test_options'
		)
		assert result.rc == 0

		# Check that it made it into the database
		result = host.run('stack list host interface backend-0-0 output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [{
			'channel': None,
			'default': None,
			'host': 'backend-0-0',
			'interface': 'eth0',
			'ip': None,
			'mac': '00:11:22:33:44:55',
			'module': None,
			'name': None,
			'network': 'test',
			'options': 'test_options',
			'vlan': None
		}]

	def test_multiple_hosts(self, host, add_host_with_interface):
		# Add a second test backend
		add_host_with_interface('backend-0-1', '0', '1', 'backend', 'eth0')

		# Set the host interface options on both backends
		result = host.run(
			'stack set host interface options backend-0-0 backend-0-1 '
			'interface=eth0 options=test_options'
		)
		assert result.rc == 0

		# Check that the changes made it into the database
		result = host.run('stack list host interface a:backend output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [
			{
				'channel': None,
				'default': None,
				'host': 'backend-0-0',
				'interface': 'eth0',
				'ip': None,
				'mac': None,
				'module': None,
				'name': None,
				'network': None,
				'options': 'test_options',
				'vlan': None
			},
			{
				'channel': None,
				'default': None,
				'host': 'backend-0-1',
				'interface': 'eth0',
				'ip': None,
				'mac': None,
				'module': None,
				'name': None,
				'network': None,
				'options': 'test_options',
				'vlan': None
			}
		]
