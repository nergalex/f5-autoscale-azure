#!/usr/bin/python
#
# Copyright (c) 2016 Matt Davis, <mdavis@ansible.com>
#                    Chris Houseknecht, <house@redhat.com>

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_networkinterface_info

version_added: "2.9"

short_description: Get a network VMSS interface facts

description:
    - Get facts for a specific network interface within a VMSS.

options:
    resource_group_name:
        description:
            - Name of ...
    virtual_machine_scale_set_name:
        description:
            - Name of ...
    virtualmachine_index:
        description:
            - Name of ...
    network_interface_name:
        description:
            - Name of ...

extends_documentation_fragment:
    - azure

author:
    - Nergalex (@Nergalex)

'''

EXAMPLES = '''
    - name: Get facts for one network interface
      azure_rm_networkinterface_vmss_info:
        resource_group_name: rg-Inbound
        virtual_machine_scale_set_name: awaf
        virtualmachine_index: 1
        network_interface_name: awaf-management

'''

RETURN = '''
azure_networkinterfaces:
    description:
        - List of network interface dicts.
    returned: always
    type: list
    example: 
    'networkinterfaces': [
		{
		'subnet': 'net-TotalInbound-management', 
		'dns_servers': [], 
		'name': 'awaf-management', 
		'resource_group': 'rg-TotalInbound', 
		'tags': None, 
		'enable_accelerated_networking': False, 
		'provisioning_state': 'Succeeded', 
		'dns_settings': {
			'dns_servers': [], 'internal_fqdn': None, 'internal_dns_name_label': None, 'applied_dns_servers': []
		}, 
		'location': None, 
		'mac_address': '00-0D-3A-7A-AF-21', 
		'security_group': None, 
		'virtual_network': {
			'name': 'vnet-TotalInbound', 
			'resource_group': 'rg-TotalInbound'
		}, 
		'ip_configurations': [
			{
			'public_ip_address': None, 
			'primary': True, 
			'private_ip_address': '10.100.0.6', 
			'load_balancer_backend_address_pools': None, 
			'private_ip_allocation_method': 'Dynamic', 
			'application_security_groups': None, 
			'name': 'management'
			}
		], 
		'enable_ip_forwarding': False, 
		'id': '/subscriptions/1005fe30-e19e-4091-8480-8b61ecb8106e/resourceGroups/rg-TotalInbound/providers/Microsoft.Compute/virtualMachineScaleSets/awaf/virtualMachines/1/networkInterfaces/awaf-management'
		}
		]
	}
	]
	
networkinterfaces:
    description:
        - List of network interface dicts. Each dict contains parameters can be passed to M(azure_rm_networkinterface) module.
    type: list
    returned: always
    contains:
        id:
            description:
                - Id of the network interface.
        resource_group:
            description:
                - Name of a resource group where the network interface exists.
        name:
            description:
                - Name of the network interface.
        location:
            description:
                - Azure location.
        virtual_network:
            description:
                - An existing virtual network with which the network interface will be associated.
                - It is a dict which contains I(name) and I(resource_group) of the virtual network.
        subnet:
            description:
                - Name of an existing subnet within the specified virtual network.
        tags:
            description:
                - Tags of the network interface.
        ip_configurations:
            description:
                - List of IP configurations, if contains multiple configurations.
            contains:
                name:
                    description:
                        - Name of the IP configuration.
                private_ip_address:
                    description:
                        - Private IP address for the IP configuration.
                private_ip_allocation_method:
                    description:
                        - Private IP allocation method.
                public_ip_address:
                    description:
                        - Name of the public IP address. None for disable IP address.
                public_ip_allocation_method:
                    description:
                        - Public IP allocation method.
                load_balancer_backend_address_pools:
                    description:
                        - List of existing load-balancer backend address pools to associate with the network interface.
                primary:
                    description:
                        - Whether the IP configuration is the primary one in the list.
                application_security_groups:
                    description:
                        - List of Application security groups.
                    sample: /subscriptions/<subsid>/resourceGroups/<rg>/providers/Microsoft.Network/applicationSecurityGroups/myASG
        enable_accelerated_networking:
            description:
                - Specifies whether the network interface should be created with the accelerated networking feature or not.
        create_with_security_group:
            description:
                - Specifies whether a default security group should be be created with the NIC. Only applies when creating a new NIC.
            type: bool
        security_group:
            description:
                - A security group resource ID with which to associate the network interface.
        enable_ip_forwarding:
            description:
                - Whether to enable IP forwarding
        dns_servers:
            description:
                - Which DNS servers should the NIC lookup.
                - List of IP addresses.
        mac_address:
            description:
                - The MAC address of the network interface.
        provisioning_state:
            description:
                - The provisioning state of the network interface.
        dns_settings:
            description:
                - The DNS settings in network interface.
            contains:
                dns_servers:
                    description:
                        - List of DNS servers IP addresses.
                applied_dns_servers:
                    description:
                        - If the VM that uses this NIC is part of an Availability Set, then this list will have the union of all DNS servers
                          from all NICs that are part of the Availability Set. This property is what is configured on each of those VMs.
                internal_dns_name_label:
                    description:
                        - Relative DNS name for this NIC used for internal communications between VMs in the same virtual network.
                internal_fqdn:
                    description:
                        - Fully qualified DNS name supporting internal communications between VMs in the same virtual network.
'''  # NOQA
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.common import AzureMissingResourceHttpError, AzureHttpError
except Exception:
    # This is handled in azure_rm_common
    pass

from ansible.module_utils.azure_rm_common import AzureRMModuleBase, azure_id_to_dict


AZURE_OBJECT_CLASS = 'NetworkInterface'


def nic_to_dict(nic):
    ip_configurations = [
        dict(
            name=config.name,
            private_ip_address=config.private_ip_address,
            private_ip_allocation_method=config.private_ip_allocation_method,
            primary=config.primary,
            load_balancer_backend_address_pools=([item.id for item in config.load_balancer_backend_address_pools]
                                                 if config.load_balancer_backend_address_pools else None),
            public_ip_address=config.public_ip_address.id if config.public_ip_address else None,
            application_security_groups=([asg.id for asg in config.application_security_groups]
                                         if config.application_security_groups else None)
        ) for config in nic.ip_configurations
    ]
    config = nic.ip_configurations[0] if len(nic.ip_configurations) > 0 else None
    subnet_dict = azure_id_to_dict(config.subnet.id) if config and config.subnet else None
    subnet = subnet_dict.get('subnets') if subnet_dict else None
    virtual_network = dict(
        resource_group=subnet_dict.get('resourceGroups'),
        name=subnet_dict.get('virtualNetworks')) if subnet_dict else None
    return dict(
        id=nic.id,
        resource_group=azure_id_to_dict(nic.id).get('resourceGroups'),
        name=nic.name,
        subnet=subnet,
        virtual_network=virtual_network,
        location=nic.location,
        tags=nic.tags,
        security_group=nic.network_security_group.id if nic.network_security_group else None,
        dns_settings=dict(
            dns_servers=nic.dns_settings.dns_servers,
            applied_dns_servers=nic.dns_settings.applied_dns_servers,
            internal_dns_name_label=nic.dns_settings.internal_dns_name_label,
            internal_fqdn=nic.dns_settings.internal_fqdn
        ),
        ip_configurations=ip_configurations,
        mac_address=nic.mac_address,
        enable_ip_forwarding=nic.enable_ip_forwarding,
        provisioning_state=nic.provisioning_state,
        enable_accelerated_networking=nic.enable_accelerated_networking,
        dns_servers=nic.dns_settings.dns_servers,
    )


class AzureRMNetworkInterfaceInfo(AzureRMModuleBase):

    def __init__(self):

        self.module_arg_spec = dict(
            resource_group_name=dict(type='str'),
            virtual_machine_scale_set_name=dict(type='str'),
            virtualmachine_index=dict(type='int'),
            network_interface_name=dict(type='str')
        )

        self.results = dict(
            changed=False,
        )

        self.resource_group_name = None
        self.virtual_machine_scale_set_name = None
        self.virtualmachine_index = None
        self.network_interface_name = None

        super(AzureRMNetworkInterfaceInfo, self).__init__(self.module_arg_spec,
                                                          supports_tags=False,
                                                          facts_module=True
                                                          )

    def exec_module(self, **kwargs):

        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if self.virtual_machine_scale_set_name and not self.resource_group_name:
            self.fail("Parameter error: resource group required when filtering by name.")

        results = [self.get_item()]

        self.results['networkinterfaces'] = self.to_dict_list(results)
        return self.results

    def get_item(self):
        self.log('Get properties for {0}'.format(self.network_interface_name))
        item = None
        try:
            item = self.network_client.network_interfaces.get_virtual_machine_scale_set_network_interface(
                resource_group_name=self.resource_group_name,
                virtual_machine_scale_set_name=self.virtual_machine_scale_set_name,
                virtualmachine_index=self.virtualmachine_index,
                network_interface_name=self.network_interface_name
            )
        except Exception:
            pass

        return item

    def to_dict_list(self, raws):
        return [nic_to_dict(item) for item in raws] if raws else []


def main():
    AzureRMNetworkInterfaceInfo()


if __name__ == '__main__':
    main()
