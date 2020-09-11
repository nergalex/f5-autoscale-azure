Autoscale F5 products in Microsoft Azure
==================================================
.. contents:: Table of Contents

Summary
==================================================
Use Case
###############
- **Cost** -- securise access to your applications by centralizing Security features in an Edge Security infrastructure
- **Security** -- use adaptative security features - editor agnostic - depending on the criticality of your assets (Defense in Depth methodology)
- **Multi-tenancy** -- manage and monitor each Application individually like a dedicated infrastructure (RBAC feature)
- **Resiliency** -- deploy Applications in Multi-regions and/or Multi-clouds by automating deployment of your infrastructure as a replicate
- **Reliability** -- deploy Applications using Canary or A/B testing on your infrastructure replicate (GSLB feature)
- **Dynamism** -- update configuration based on upstream server life cycle by using Service Discovery feature at Edge

Benefit
###############
- **Cost** -- maximize CPU consumption of Security assets
- **unlock Security** -- be free to use and change Security feature products in data path at Edge, transparently for Application owners
- **Multi-tenancy** -- offer an Edge Security as a managed service for Application development team and hide infrastructure management owned by for DevSecOps team
- **Resiliency** -- deploy on specific Edge replicates depending on the Service Level Objective of each Application (end-user latency, availability...)
- **Reliability** -- prevent CPU and upstream port exhaustion by setting CPU and outbound flows as a metric in scaling policy
- **Observability** -- deploy Edge Security replicate in closest regions of your end-users and monitor metrics and security events for global visibility

Architecture
###############
The Edge Security architecture described in this article is a solution based on specific customer needs, business expectation and security requirements.
There is no unique solution, please follow the methodology presented in the Secure Cloud Architecture webinar, available in
`English <https://gateway.on24.com/wcc/eh/1140560/lp/2200026/f5-emea-webinar-march-2020-english>`_,
`French <https://gateway.on24.com/wcc/eh/1140560/lp/2209631/f5-emea-webinar-march-2020-french>`_
or other `languages  <https://www.f5.com/c/emea-2020/emea-webinar-library>`_.
Feel free to reach `F5 people <https://www.linkedin.com/company/f5/people/>`_ for a dedicated workshop.

.. figure:: _figure/Architecture_INBOUND.png

Ecosystem
*********************
- NGINX+
- NGINX App Protect
- NGINX Controller
- NGINX Unit
- BIG-IP Advanced WAF
- BIG-IQ
- Ansible Tower
- Consul by Hashicorp

Design Consideration
*********************
Ths article is to propose a solution based on:

- native cloud provider autoscaling feature
- F5 Controller products for Out Of Band management and Analytics
- customer eco-system products

For autoscale need in a another customer context,
`ARM templates <https://github.com/F5Networks/f5-azure-arm-templates>`_ - supported by F5 - could be sufficient.

Automation tool used here is `Ansible <https://github.com/F5Networks/f5-ansible>`_. F5 products can also be deployed with `Terraform <https://github.com/F5Networks/terraform-provider-bigip-version0.12>`_, refer to those good `articles written by Jeff Giroux <https://github.com/JeffGiroux/f5_terraform>`_

Demo
###############
- Automate an Application deployment
.. raw:: html

    <a href="http://www.youtube.com/watch?v=p1rfhssaE_U"><img src="http://img.youtube.com/vi/p1rfhssaE_U/0.jpg" width="600" height="400" title="Automate an Application deployment" alt="Automate an Application deployment"></a>

- Scale Out VMSS NGINX+ managed by NGINX Controller
.. raw:: html

    <a href="http://www.youtube.com/watch?v=x4CnlKm_Ik8"><img src="http://img.youtube.com/vi/x4CnlKm_Ik8/0.jpg" width="600" height="400" title="Scale Out VMSS NGINX+ managed by NGINX Controller" alt="Scale Out VMSS NGINX+ managed by NGINX Controller"></a>

- Scale In VMSS NGINX+ managed by NGINX Controller
.. raw:: html

    <a href="http://www.youtube.com/watch?v=8tG1QF0Rurw"><img src="http://img.youtube.com/vi/8tG1QF0Rurw/0.jpg" width="600" height="400" title="Scale In VMSS NGINX+ managed by NGINX Controller" alt="Scale In VMSS NGINX+ managed by NGINX Controller"></a>

- Scale Out VMSS BIG-IP managed by BIG-IQ
.. raw:: html

    <a href="http://www.youtube.com/watch?v=EvSrmwhDP2o"><img src="http://img.youtube.com/vi/EvSrmwhDP2o/0.jpg" width="600" height="400" title="Scale Out VMSS BIG-IP managed by BIG-IQ" alt="Scale Out VMSS BIG-IP managed by BIG-IQ"></a>

- Scale Out VMSS BIG-IP managed by BIG-IQ
.. raw:: html

    <a href="http://www.youtube.com/watch?v=-zzKjA_mFIY"><img src="http://img.youtube.com/vi/-zzKjA_mFIY/0.jpg" width="600" height="400" title="Scale In VMSS BIG-IP managed by BIG-IQ" alt="Scale In VMSS BIG-IP managed by BIG-IQ"></a>

Pre-requisites
==============
Ansible Tower
##############
virtualenv
**************
Create a virtualenv, follow
`Tower admin guide <https://docs.ansible.com/ansible-tower/latest/html/administration/tipsandtricks.html#preparing-a-new-custom-virtualenv>`_
Install ansible >= 2.9

.. code:: bash

    $ sudo yum groupinstall -y "development tools"
    $ sudo virtualenv /var/lib/awx/venv/my_env
    $ sudo /var/lib/awx/venv/my_env/bin/pip install python-memcached psutil
    $ sudo /var/lib/awx/venv/my_env/bin/pip install -U ansible

Ensure that your virtualenv have the rights 755, else:

.. code:: bash
    $ chmod 755 -R /var/lib/awx/venv/my_env

F5 f5devcentral.f5ansible
*************************
This collection includes the most recently released ansible modules for BIG-IP and BIG-IQ from F5Networks.
This collection packages and distributes playbooks, roles, modules, and plugins.
source: `Ansible galaxy <https://galaxy.ansible.com/f5networks/f5_modules>`_

.. code:: bash
    $ sudo ansible-galaxy collection install f5networks.f5_modules -p /usr/share/ansible/collections

Azure azure_preview_modules
***************************
This role is the most complete and includes all the latest Azure modules. The update and bug fix are done in a more timely manner than official Ansible release.
If you use Ansible for Azure resource provisioning purpose, you're strongly encouraged to install this role.
Follow `install guide <https://github.com/Azure/azure_preview_modules>`_

.. code:: bash
    $ sudo ansible-galaxy install azure.azure_preview_modules
    $ sudo /var/lib/awx/venv/my_env/bin/pip install -U -r /etc/ansible/roles/azure.azure_preview_modules/files/requirements-azure.txt
    $ sudo /var/lib/awx/venv/my_env/bin/pip show azure-mgmt-compute

If ``azure-mgmt-compute`` < ``10.0.0`` then use last update from azure_preview_modules repo and not from Galaxy.
``/etc/ansible/roles/`` is an example of an Tower installation where ``roles`` are located.

.. code:: bash
    $ sudo cd /etc/ansible/roles/
    $ sudo git clone https://github.com/Azure/azure_preview_modules.git
    $ sudo /var/lib/awx/venv/my_env/bin/pip install -r /etc/ansible/roles/azure.azure_preview_modules/files/requirements-azure.txt
    $ sudo vi /etc/ansible/roles/azure.azure_preview_modules/defaults/main.yml
        skip_azure_sdk: false

Custom module for azure_preview_modules
***************************************
Copy modules below to ``/etc/ansible/roles/azure.azure_preview_modules/library/``:

- ``azure_rm_autoscale.py`` (if not `fix <https://github.com/ansible-collections/azure/issues/120>`_ applied)
- ``azure_rm_networkinterface_vmss_info.py``
- ``azure_rm_virtualmachinescaleset_2NIC.py``
- ``azure_rm_virtualmachinescalesetinstance_info.py``

VMSS credential
***************
Create custom credential `cred_NGINX` to manage access to VMs in VMSS

=====================================================   =============================================       =============================================   =============================================   =============================================
REDENTIAL TYPE                                            USERNAME                                           SSH PRIVATE KEY                                        SIGNED SSH CERTIFICATE                                        PRIVILEGE ESCALATION METHOD
=====================================================   =============================================       =============================================   =============================================   =============================================
``Machine``                                             ``my_VM_admin_user``                                ``my_VM_admin_user_key``                        ``my_VM_admin_user_CRT``                        ``sudo``
=====================================================   =============================================       =============================================   =============================================   =============================================

Role structure
**************
- Deployment is based on ``workflow template``. Example: ``workflow template``=``wf-create_create_edge_security_inbound`` ;
- A ``workflow template`` includes multiple ``job template``. Example: ``job template``=``poc-azure_create_hub_edge_security_inbound``
- A ``job template`` have an associated ``playbook``. Example: ``playbook``=``playbooks/poc-azure.yaml``
- A ``playbook`` launch a ``play`` in a ``role``. Example: ``role``=``poc-azure``

.. code:: yaml

    - hosts: localhost
      gather_facts: no
      roles:
        - role: poc-azure

- A ``play`` is an ``extra variable`` named ``activity`` and set in each ``job template``. Example: ``create_hub_edge_security_inbound``
- The specified ``play`` (or ``activity``) is launched by the ``main.yaml`` task located in the role ``tasks/main.yaml``

.. code:: yaml

    - name: Run specified activity
      include_tasks: "{{ activity }}.yaml"
      when: activity is defined

- The specified ``play`` contains ``tasks`` to execute. Example: play=``create_hub_edge_security_inbound.yaml``

Consul by Hashicorp
###################
Refer to this `article <https://github.com/nergalex/f5-sslo-category#consul>`_ to install Consul.

Deploy a Edge Security replica
==================================================
1. Azure - network components
###############

Create and launch a workflow template ``wf-create_create_edge_security_inbound`` that include those Job templates in this order:
In ``poc-azure_create_hub_edge_security_inbound``, remove ``virtual_network_gateway`` task and routes to ``virtual_network_gateway`` if a vNet peering is used to interconnect your cross-management vNet.

==============================================  =============================================   =============================================   =============================================   =============================================   =============================================
Job template                                    playbook                                        activity                                        inventory                                       limit                                           credential
==============================================  =============================================   =============================================   =============================================   =============================================   =============================================
``poc-azure_create_hub_edge_security_inbound``  ``playbooks/poc-azure.yaml``                    ``create_hub_edge_security_inbound``            ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_create-vm-nginx_unit``              ``playbooks/poc-azure.yaml``                    ``create-vm-nginx_unit``                        ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-nginx_onboarding_system_vm``              ``playbooks/poc-nginx_vm.yaml``                 ``onboarding_system``                           ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-nginx_onboarding_nginx_unit``             ``playbooks/poc-azure.yaml``                    ``onboarding_nginx_unit``                       ``localhost``                                   ``localhost``                                   ``cred_NGINX``
==============================================  =============================================   =============================================   =============================================   =============================================   =============================================

==============================================  =============================================   =============================================
Extra variable                                  Description                                     Example
==============================================  =============================================   =============================================
``extra_availability_zone``                     availability zones                              ``[1, 2]``
``extra_external_subnet_address_prefix``        BIG-IP dataplane subnet                         ``10.100.2.0/24``
``extra_internal_subnet_address_prefix``        NGINX South dataplane subnet                    ``10.100.2.0/24``
``extra_gateway_subnet_address_prefix``         Subnet dedicated to VPN GW                      ``10.100.255.0/24``
==============================================  =============================================   =============================================

2. NGINX App Protect - WAF
###############
Create and launch a workflow template ``wf-create_vmss_nginx_app_protect`` that include those Job templates in this order:

=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
Job template                                            objective                                           playbook                                        activity                                        inventory                                       limit                                           credential
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
``poc-azure_create-vmss-nginx-2NIC_1LB``                Create VMSS                                         ``playbooks/poc-azure.yaml``                    ``create-vmss-nginx-2NIC_1LB``                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_set-vmss-master_vm``                        Set a Master VM                                     ``playbooks/poc-azure.yaml``                    ``set-vmss-master_vm``                          ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_create-vmss-extension-nginx_app_protect``   Set script to install NGINX App Protect             ``playbooks/poc-azure.yaml``                    ``create-vmss-extension-nginx_app_protect``     ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_get-vmss-facts``                            Get VM IPs from VMSS                                ``playbooks/poc-azure.yaml``                    ``get-vmss-facts``                              ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-nginx_onboarding_system``                         Configure system variable                           ``playbooks/poc-azure.yaml``                    ``onboarding_system``                           ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-nginx_onboarding_nginx_app_protect``              Configure NGINX App Protect                         ``playbooks/poc-azure.yaml``                    ``onboarding_nginx_app_protect``                ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-azure_create-vmss-autoscale``                     Create an autoscale policy                          ``playbooks/poc-azure.yaml``                    ``create-vmss-autoscale``                       ``my_project``                                  ``localhost``                                   ``my_vmss_credential``
``poc-nginx_onboarding_nginx_sync_step1_master``        Configure Master VM as a Master NGINX               ``playbooks/poc-nginx_master.yaml``             ``onboarding_nginx_sync_step1_master``          ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-nginx_onboarding_nginx_sync_step2_slaves``        Configure Slaves VM as a Slave NGINX                ``playbooks/poc-nginx_slaves.yaml``             ``onboarding_nginx_sync_step2_slaves``          ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-nginx_onboarding_nginx_sync_step3_master``        Copy from Master VM to Slave NGINX                  ``playbooks/poc-nginx_master.yaml``             ``onboarding_nginx_sync_step3_master``          ``localhost``                                   ``localhost``                                   ``cred_NGINX``
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================

==============================================  =============================================   =========================================================
Extra variable                                  Description                                     Example
==============================================  =============================================   =========================================================
``extra_app_protect_monitor_ip``                Kibana for NGINX App Protect                    ``10.0.0.20``
``extra_app_protect_repo``                      repo that stores NAP install scripts            ``http://10.0.0.19``
``extra_availability_zone``                     availability zones                              ``[1, 2]``
``extra_dataplane_subnet_address_mask``         eth1 subnet mask                                ``24``
``extra_elb_management_name``                   ELB for outbound connection during install      ``outbound-management-vmss-nginx-external``
``extra_gw_dataplane``                          eth1 GW                                         ``10.100.1.1``
``extra_gw_management``                         eth0 GW                                         ``10.100.0.1``
``extra_key_data``                              admin CRT                                       ``-----BEGIN  ... CERTIFICATE-----``
``extra_lb_dataplane_name``                     LB name for dataplane traffic                   ``external``
``extra_lb_dataplane_type``                     LB type for dataplane traffic                   ``elb``
``extra_location``                              region                                          ``eastus2``
``extra_offer``                                 OS                                              ``CentOS``
``extra_publisher``                             OS distrib                                      ``OpenLogic``
``extra_sku``                                   OS distrib version                              ``7.4``
``extra_vm_size``                               VM type                                         ``Standard_DS3_v2``
``extra_vmss_capacity``                         initial vmss_capacity                           `2``
``extra_vmss_name``                             logical vmss_name                               ``nginxwaf``
``nginx_rpm_version``                           Nginx+ version to install                       ``20``
``extra_platform_name``                         logical platform_name                           ``myPlatform``
``extra_platform_tags``                         logical platform_tags                           ``environment=DMO ...``
``extra_project_name``                          logical project_name                            ``CloudBuilderf5``
``extra_route_prefix_on_premise``               cross management subnet                         ``10.0.0.0/24``
``extra_subnet_dataplane_name``                 logical name for eth1 subnet                    ``nginx``
``extra_template_nginx_conf``                   jinja2 template for nginx.conf                  ``nginx_app_protect.conf``
``extra_template_route``                        jinja2 template for persistent route            ``system_route_persistent-default_via_dataplane.conf``
``extra_app_protect_monitor_ip``                IP address of Kibana server                     ``10.0.0.20``
``extra_nginx_key``                             NGINX+ private key (PEM format)                 ``-----BEGIN  ... KEY-----``
``extra_nginx_crt``                             NGINX+ certificate (PEM format)                 ``-----BEGIN  ... CERTIFICATE-----``
``extra_webhook_email``                         e-mail address                                  ``admin@acme.com``
``extra_webhook_vm_name``                       VM name                                         ``autoscale-f5``
==============================================  =============================================   =========================================================


3. BIG-IP - Advanced WAF
###############

Create and launch a workflow template ``wf-create_vmss_device-group_awaf`` that include those Job templates in this order:

=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
Job template                                            objective                                           playbook                                        activity                                        inventory                                       limit                                           credential
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
``poc-azure_create-vmss-bigip``                         CREATE a VMSS                                       ``playbooks/poc-azure.yaml``                    ``create-vmss-bigip``                                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_set-vmss-master_vm``                        Protect a VM 'master' from scale in action          ``playbooks/poc-azure.yaml``                    ``set-vmss-master_vm``                                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_get-vmss-facts``                            GET VMSS IPs                                        ``playbooks/poc-azure.yaml``                    ``get-vmss-facts``                                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-f5_do_vmss_device-group``                         Onboard BIG-IP                                      ``playbooks/poc-f5.yaml``                       ``do_vmss_device-group``                                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-f5-as3_vmss_device-group_create_log_profile``     CREATE shared ASM log profile                       ``playbooks/poc-f5.yaml``                       ``as3_vmss_device-group_create``                                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-f5-bigiq_vmss_device-group_discover``             Discover BIG-IP by BIG-IQ                           ``playbooks/poc-f5.yaml``                       ``bigiq_vmss_device-group_discover``                                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_create-vmss-autoscale``                     CREATE autoscaling policy                           ``playbooks/poc-azure.yaml``                    ``create-vmss-autoscale``                                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================

==============================================  =============================================   =========================================================
Extra variable                                  Description                                     Example
==============================================  =============================================   =========================================================
``extra_admin_user``                            admin user name on BIG-IP                       ``admin``
``extra_admin_password``                        admin user password on BIG-IP                   ``Ch4ngeMe!``
``extra_port_mgt``                              management port on BIG-IP                       ``443``
``extra_key_data``                              admin CRT                                       ``-----BEGIN  ... CERTIFICATE-----``
``extra_offer``                                 offer                                           ``f5-big-ip-byol``
``extra_sku``                                   OS distrib version                              ``7.4``
``extra_vm_size``                               VM type                                         ``Standard_DS4_v2``
``extra_device_modules``                        List of modules to discover by BIG-IQ           ``ltm,asm,security_shared``
``extra_as3_template``                          AS template to deploy                           ``as3_security_logging.jinja2``
``extra_availability_zone``                     availability zones                              ``[1, 2]``
``extra_bigiq_admin_password``                                                                  ``Ch4ngeMe!``
``extra_bigiq_admin_user``                                                                      ``admin``
``extra_bigiq_device_discovery_state``                                                          ``present``
``extra_bigiq_ip_mgt``                                                                          ``10.0.0.27``
``extra_bigiq_port_mgt``                                                                        ``443``
``extra_dataplane_subnet_address_mask``         eth1 subnet mask                                ``24``
``extra_dcd_ip``                                BIG-IQ lognode IP                               ``10.0.0.28``
``extra_dcd_port``                              BIG-IQ lognode port                             ``8514``
``extra_dcd_servers``                           BIG-IQ lognode servers or ILB VIP for ASM log   ``[{''address'': ''10.0.0.28'', ''port'': ''8514''}]``
``extra_elb_management_name``                   ELB for outbound connection during install      ``outbound-management-vmss-awaf``
``extra_gw_dataplane``                          eth1 GW                                         ``10.100.2.1``
``extra_gw_management``                         eth0 GW                                         ``10.100.0.1``
``extra_lb_dataplane_name``                     LB name for dataplane traffic                   ``external``
``extra_lb_dataplane_type``                     LB type for dataplane traffic                   ``ilb``
``extra_licensing``                             Licencing model for BIG-IP                      ``BIGIQ``
``extra_location``                              Azure region                                    ``eastus2``
``extra_platform_name``                         logical platform_name                           ``myPlatform``
``extra_platform_tags``                         logical platform_tags                           ``environment=DMO ...``
``extra_project_name``                          logical project_name                            ``CloudBuilderf5``
``extra_route_prefix_on_premise``               cross management subnet                         ``10.0.0.0/24 ``
``extra_subnet_dataplane_name``                 logical name for eth1 subnet                    ``external``
``extra_template_do``                                                                           ``do-vmss-standalone-2nic-awaf-BIGIQ.json``
``extra_upstream_lb_vip``                       upstream server or ILB or AppGW                 ``10.100.3.10``
``extra_vmss_capacity``                         initial vmss_capacity                           ``2``
``extra_vmss_name``                             logical vmss_name                               ``awaf``
``extra_webhook_email``                         e-mail address                                  ``admin@acme.com``
``extra_webhook_vm_name``                       VM name                                         ``autoscale-f5``
==============================================  =============================================   =========================================================

4. NGINX+ - API GW
###############
Create and launch a workflow template ``wf-create_vmss_nginx_apigw`` that include those Job templates in this order:

=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
Job template                                            objective                                           playbook                                        activity                                        inventory                                       limit                                           credential
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
``poc-azure_create-vmss-nginx-2NIC_2LB``                Create VMSS                                         ``playbooks/poc-azure.yaml``                    ``create-vmss-nginx-2NIC_2LB``                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_set-vmss-master_vm``                        Set a Master VM                                     ``playbooks/poc-azure.yaml``                    ``set-vmss-master_vm``                          ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_create-vmss-extension-nginx_from_repo``     Set script to install NGINX+                        ``playbooks/poc-azure.yaml``                    ``create-vmss-extension-nginx_from_repo``     ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_get-vmss-facts``                            Get VM IPs from VMSS                                ``playbooks/poc-azure.yaml``                    ``get-vmss-facts``                              ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-nginx_onboarding_system``                         Configure system variable                           ``playbooks/poc-azure.yaml``                    ``onboarding_system``                           ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-nginx_onboarding_nginx_adc``                      Configure NGINX App Protect                         ``playbooks/poc-azure.yaml``                    ``onboarding_nginx_app_protect``                ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-azure_create-vmss-autoscale``                     Create an autoscale policy                          ``playbooks/poc-azure.yaml``                    ``create-vmss-autoscale``                       ``my_project``                                  ``localhost``                                   ``my_vmss_credential``
``poc-nginx_onboarding_nginx_sync_step1_master``        Configure Master VM as a Master NGINX               ``playbooks/poc-nginx_master.yaml``             ``onboarding_nginx_sync_step1_master``          ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-nginx_onboarding_nginx_sync_step2_slaves``        Configure Slaves VM as a Slave NGINX                ``playbooks/poc-nginx_slaves.yaml``             ``onboarding_nginx_sync_step2_slaves``          ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-nginx_onboarding_nginx_sync_step3_master``        Copy from Master VM to Slave NGINX                  ``playbooks/poc-nginx_master.yaml``             ``onboarding_nginx_sync_step3_master``          ``localhost``                                   ``localhost``                                   ``cred_NGINX``
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================

==============================================  =============================================   =========================================================
Extra variable                                  Description                                     Example
==============================================  =============================================   =========================================================
``extra_app_protect_monitor_ip``                Kibana for NGINX App Protect                    ``10.0.0.20``
``extra_app_protect_repo``                      repo that stores NAP install scripts            ``http://10.0.0.19``
``extra_availability_zone``                     availability zones                              ``[1, 2]``
``extra_dataplane_subnet_address_mask``         eth1 subnet mask                                ``24``
``extra_elb_management_name``                   ELB for outbound connection during install      ``outbound-management-vmss-nginx-external``
``extra_gw_dataplane``                          eth1 GW                                         ``10.100.1.1``
``extra_gw_management``                         eth0 GW                                         ``10.100.0.1``
``extra_key_data``                              admin CRT                                       ``-----BEGIN  ... CERTIFICATE-----``
``extra_lb_dataplane_name``                     LB name for dataplane traffic                   ``external``
``extra_lb_dataplane_type``                     LB type for dataplane traffic                   ``elb``
``extra_location``                              region                                          ``eastus2``
``extra_offer``                                 OS                                              ``CentOS``
``extra_publisher``                             OS distrib                                      ``OpenLogic``
``extra_sku``                                   OS distrib version                              ``7.4``
``extra_vm_size``                               VM type                                         ``Standard_DS3_v2``
``extra_vmss_capacity``                         initial vmss_capacity                           `2``
``extra_vmss_name``                             logical vmss_name                               ``nginxwaf``
``nginx_rpm_version``                           Nginx+ version to install                       ``20``
``extra_platform_name``                         logical platform_name                           ``myPlatform``
``extra_platform_tags``                         logical platform_tags                           ``environment=DMO ...``
``extra_project_name``                          logical project_name                            ``CloudBuilderf5``
``extra_route_prefix_on_premise``               cross management subnet                         ``10.0.0.0/24``
``extra_subnet_dataplane_name``                 logical name for eth1 subnet                    ``nginx``
``extra_template_nginx_conf``                   jinja2 template for nginx.conf                  ``nginx_adc.conf``
``extra_template_route``                        jinja2 template for persistent route            ``system_route_persistent-default_via_mgmtplane.conf``
``extra_app_protect_monitor_ip``                IP address of Kibana server                     ``10.0.0.20``
``extra_webhook_email``                         e-mail address                                  ``admin@acme.com``
``extra_webhook_vm_name``                       VM name                                         ``autoscale-f5``
``extra_vip_address_list_nginx_second_line``    routed subnet for VIP                           ``[10.100.11.0/24]``
==============================================  =============================================   =========================================================

5. NGINX Unit - webhook
###############
Create a dedicated user *webhook* on Tower that have rights to only execute Autoscale workflows.
Code embedded in webhook are available `here <https://github.com/nergalex/webhook_public>`_.
Create and launch a workflow template ``wf-create_create_vm_app_nginx_unit`` that include those Job templates in this order:

=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
Job template                                            objective                                           playbook                                        activity                                        inventory                                       limit                                           credential
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
``poc-azure_create-vm-nginx_unit``                      Create a VM                                         ``playbooks/poc-azure.yaml``                    ``create-vm-nginx_unit``                        ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-onboarding_nginx_unit_faas_autoscale``            Deploy an Webhook App                               ``playbooks/poc-nginx_vm.yaml``                 ``onboarding_nginx_unit_faas_autoscale``        ``localhost``                                                                                   ``cred_NGINX``
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================

==============================================  =============================================   ================================================================================================================================================================================================================
Extra variable                                  Description                                     Example
==============================================  =============================================   ================================================================================================================================================================================================================
``extra_vm_name``                               VM name                                         ``autoscale-f5``
``extra_vm_ip_mgt``                                                                             ``10.100.0.10``
``extra_vm_size``                                                                               ``Standard_B4ms``
``extra_availability_zone``                     availabiltity zones                             ``[1, 2]``
``infra_admin_username``                        admin user name                                 ``-----BEGIN  CERTIFICATE-----XXXXXXX-----END CERTIFICATE-----``
``extra_key_data``                              admin CRT to secure admin user access to VM     ``-----BEGIN  CERTIFICATE-----XXXXXXX-----END CERTIFICATE-----``
``extra_location``                              region. Set by webhook                          ``eastus2``
``extra_platform_name``                         logical platform_name                           ``myPlatform``
``extra_platform_tags``                                                                         ``environment=DMO project=CloudBuilderf5``
``extra_route_prefix_on_premise``               cross management subnet                         ``10.0.0.0/24``
``extra_tower_hostname``                                                                        ``1.1.1.1``
``extra_tower_username``                                                                        ``webhook-login``
``extra_tower_password``                                                                        ``*****************``
``extra_tower_client_id``                                                                       ``*****************``
``extra_tower_client_secret``                                                                   ``******************``
``extra_webhook_ca_pem``                                                                        ``-----BEGIN CERTIFICATE...``
``extra_webhook_cert_pem``                                                                      ``-----BEGIN CERTIFICATE...``
``extra_webhook_key_pem``                                                                       ``-----BEGIN RSA PRIVATE KEY...``
``faas_app_name``                                                                               ``f5autoscale``
``faas_app_repo``                                                                               ``https://github.com/nergalex/webhook_public.git``

Deploy an Application
==================================================
Create and launch a workflow template ``wf-create-app_inbound_awaf_device-group`` that include those Job templates in this order:

=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
Job template                                            objective                                           playbook                                        activity                                        inventory                                       limit                                           credential
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
``poc-azure_create_vmss_app``                           Create a VMSS for App hosting                       ``playbooks/poc-azure.yaml``                    ``create-vmss-app``                             ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_get-vmss_hub-facts``                        Get info of BIG-IP VMSS                             ``playbooks/poc-azure.yaml``                    ``get-vmss_hub-facts``                          ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-f5-create_as3_app_inbound_awaf_device-group``     Deploy App Service (AS3) on BIG-IP                  ``playbooks/poc-f5.yaml``                       ``as3_vmss_device-group_bigiq_create``          ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-azure_get-vmss_nginx_first_line-facts``           Get info of NGINX North VMSS                        ``playbooks/poc-azure.yaml``                    ``get-vmss_nginx_first_line-facts``             ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-nginx_create_app_app_protect``                    Deploy App Service on NGINX North                   ``playbooks/poc-nginx_master.yaml``             ``create_app_app_protect``                      ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-azure_get-vmss_nginx_second_line-facts``          Get info of NGINX South VMSS                        ``playbooks/poc-azure.yaml``                    ``get-vmss_nginx_second_line-facts``            ``localhost``                                   ``localhost``                                   ``cred_NGINX``
``poc-nginx_create_app_adc``                            Deploy App Service on NGINX South                   ``playbooks/poc-nginx_master.yaml``             ``create_app_adc``                              ``my_project``                                  ``localhost``                                   ``my_vmss_credential``
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================

==============================================  =============================================   ================================================================================================================================================================================================================
Extra variable                                  Description                                     Example
==============================================  =============================================   ================================================================================================================================================================================================================
``extra_app``                                   Config specification                            ``{'backend_servers':['10.12.1.4'], 'name':'app1', 'vip_subnet_awaf':['10.100.10.2'], 'vip_subnet_nginx':['10.100.11.2']}, 'vs_listener_port_http':'80', 'vs_listener_port_https':'443'``
``extra_app_backend``                           VM extension for VMSS App                       ``juice-shop_1nic_bootstrapping.jinja2``
``extra_app_crt``                               App private key                                 ``-----BEGIN  PRIVATE KEY-----XXXXXXX-----END PRIVATE KEY-----``
``extra_app_key``                               App certificate                                 ``-----BEGIN  CERTIFICATE-----XXXXXXX-----END CERTIFICATE-----``
``extra_app_name``                              HOST in FQDN                                    ``App1``
``extra_app_url_domain``                        domain in FQDN                                  ``f5cloudbuilder.dev``
``extra_app_vm_size``                           VM type in App VMSS                             ``Standard_B2s``
``extra_bigip_target_admin_password``           BIG-IP password for AS3 deployment              ``Ch4ngeMe!``
``extra_bigip_target_admin_user``               BIG-IP user for AS3 deployment                  ``admin``
``extra_bigip_target_port_mgt``                 BIG-IP mgt port for AS3 deployment              ``443``
``extra_bigiq_admin_password``                  BIG-IQ password for AS3 deployment              ``Ch4ngeMe!``
``extra_bigiq_admin_user``                      BIG-IQ user for AS3 deployment                  ``admin``
``extra_bigiq_ip_mgt``                          BIG-IQ ip mgt for AS3 deployment                ``10.0.0.27``
``extra_bigiq_port_mgt``                        BIG-IQ mgt port for AS3 deployment              ``443``
``extra_hub_platform_name``                     BIG-IQ mgt port for AS3 deployment              ``myPlatform``
``extra_hub_vmss_name``                         BIG-IP VMSS name                                ``awaf``
``extra_key_data``                              admin CRT                                       ``-----BEGIN  CERTIFICATE-----XXXXXXX-----END CERTIFICATE-----``
``extra_location``                                                                              ``eastus2``
``extra_log_profile``                                                                           ``/Common/Shared/asm_log_bigiq``
``extra_passphrase_b64``                        App private key passphrase in b64               ``Q01QLXBhc3NwaHJhc2U=``
``extra_platform_tags``                                                                         ``environment=DMO project=CloudBuilderf5``
``extra_pool``                                  pool specification for BIG-IP AS3               ``[{'name': 'default', 'loadBalancingMode': 'least-connections-member', 'servicePort': '80', 'serverAddresses':['10.100.11.2']}]``
``extra_spokeplatform_name``                    vNet to deploy App VMSS                         ``myDistrict``
``extra_template``                              AS3 template to use                             ``as3_vmss_bigiq-http_waf.json``
``extra_vlans``                                 BIG-IP vlan listener                            ``["/Common/external"]``
``extra_vmss_capacity``                         App VMSS capacity                               ``2``
``extra_vmss_name``                             App VMSS name                                   ``myAppVMSS``
``extra_vmss_name_nginx_first_line``            NGINX App Protect VMSS name                     ``nginxwaf``
``extra_vmss_name_nginx_second_line``           NGINX+ VMSS name `                              `nginxapigw``
``extra_waf_policy``                            WAF template policy                             ``https://raw.githubusercontent.com/nergalex/.../asm_policy.xml``
``extra_zone_name``                             subnet to attach App VMSS                       ``app``
==============================================  =============================================   ================================================================================================================================================================================================================


Autoscale
=====================
BIG-IP cluster in sync-failover
################################
Limitation: :kbd:`8 cluster members = **8 BIG-IP VM instances** in VMSS`
Benefit: **time to be operational** = Application Services deployed

Scale Out
*********
Create and launch a workflow template ``wf-scale_out_bigip`` that include those Job templates in this order:

=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
Job template                                            objective                                           playbook                                        activity                                        inventory                                       limit                                           credential
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
``poc-azure_get-vmss-facts-credential_set``             Get info of current BIG-IP VMSS                     ``playbooks/poc-azure.yaml``                    ``get-vmss_hub-facts``                          ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-f5_do_scale_out``                                 Onboard BIG-IP                                      ``playbooks/poc-f5.yaml``                       ``do_vmss_device-group``                                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-f5-bigiq_discover_scale_out``                     Discover BIG-IP by BIG-IQ                           ``playbooks/poc-f5.yaml``                       ``bigiq_vmss_device-group_discover``                                  ``my_project``                                  ``localhost``                                   ``my_azure_credential``
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================

==============================================  =============================================   ================================================================================================================================================================================================================
Extra variable                                  Description                                     Example
==============================================  =============================================   ================================================================================================================================================================================================================
``extra_admin_password``                        BIG-IP password                                 ``Ch4ngeMe!``
``extra_admin_user``                            BIG-IP admin user                               ``admin``
``extra_bigiq_admin_password``                  BIG-IQ password                                 ``Ch4ngeMe!``
``extra_bigiq_admin_user``                      BIG-IQ user                                     ``admin``
``extra_bigiq_ip_mgt``                          BIG-IQ ip mgt                                   ``10.0.0.27``
``extra_bigiq_port_mgt``                        BIG-IQ mgt port                                 ``443``
``extra_dataplane_subnet_address_mask``         eth1 subnet mask                                ``24``
``extra_device_modules``                        List of modules to discover by BIG-IQ           ``ltm,asm,security_shared``
``extra_gw_dataplane``                          eth1 GW                                         ``10.100.2.1``
``extra_gw_management``                         eth0 GW                                         ``10.100.0.1``
``extra_location``                              region. Set by webhook                          ``eastus2``
``extra_platform_name``                         logical platform_name                           ``myPlatform``
``extra_port_mgt``                              management port on BIG-IP                       ``443``
``extra_project_name``                          logical project_name                            ``CloudBuilderf5``
``extra_route_prefix_on_premise``               cross management subnet                         ``10.0.0.0/24``
``extra_vmss_name``                             vmss_name. Set by webhook                       ``awaf``
==============================================  =============================================   ================================================================================================================================================================================================================

Scale In
*********
Create and launch a workflow template ``wf-scale_in_bigip`` that include those Job templates in this order:

=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
Job template                                            objective                                           playbook                                        activity                                        inventory                                       limit                                           credential
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================
``poc-azure_get-vmss-facts-credential_set``             Get info of current BIG-IP VMSS                     ``playbooks/poc-azure.yaml``                    ``get-vmss_hub-facts``                          ``my_project``                                  ``localhost``                                   ``my_azure_credential``
``poc-f5_bigiq_get_device_scale_in``                    Define deleted BIGIP from managed device list       ``playbooks/poc-f5.yaml``                       ``bigiq_get_device_scale_in``                   ``localhost``
``poc-f5_bigiq_discover_scale_in``                      Remove BIG-IP from managed device list              ``playbooks/poc-f5.yaml``                       ``bigiq_discover_scale_in``                     ``localhost``
``poc-f5_do_scale_in``                                  Onboard existing BIG-IP (cluster change)            ``playbooks/poc-f5.yaml``                       ``bigiq_discover_scale_in``                     ``localhost``
``poc-f5_bigiq_revoke_scale_in``                        Remove BIG-IP from licence pool                     ``playbooks/poc-f5.yaml``                       ``bigiq_revoke_scale_in``                       ``localhost``
=====================================================   =============================================       =============================================   =============================================   =============================================   =============================================   =============================================

==============================================  =============================================   ================================================================================================================================================================================================================
Extra variable                                  Description                                     Example
==============================================  =============================================   ================================================================================================================================================================================================================
``extra_admin_password``                        BIG-IP password                                 ``Ch4ngeMe!``
``extra_admin_user``                            BIG-IP admin user                               ``admin``
``extra_bigiq_admin_password``                  BIG-IQ password                                 ``Ch4ngeMe!``
``extra_bigiq_admin_user``                      BIG-IQ user                                     ``admin``
``extra_bigiq_ip_mgt``                          BIG-IQ ip mgt                                   ``10.0.0.27``
``extra_bigiq_port_mgt``                        BIG-IQ mgt port                                 ``443``
``extra_dataplane_subnet_address_mask``         eth1 subnet mask                                ``24``
``extra_device_modules``                        List of modules to discover by BIG-IQ           ``ltm,asm,security_shared``
``extra_gw_dataplane``                          eth1 GW                                         ``10.100.2.1``
``extra_gw_management``                         eth0 GW                                         ``10.100.0.1``
``extra_location``                              region. Set by webhook                          ``eastus2``
``extra_platform_name``                         logical platform_name                           ``myPlatform``
``extra_port_mgt``                              management port on BIG-IP                       ``443``
``extra_project_name``                          logical project_name                            ``CloudBuilderf5``
``extra_route_prefix_on_premise``               cross management subnet                         ``10.0.0.0/24``
``extra_vmss_name``                             vmss_name. Set by webhook                       ``awaf``
==============================================  =============================================   ================================================================================================================================================================================================================

BIG-IP + Consul
#####################

- **Benefit**: no limitation on BIG-IP instances in a VMSS, except from Cloud Provider limitation
- **Pain point**: time to be operational = Application Services deployed

:kbd:`ToDo`

NGINX+ without Controller
#########################

:kbd:`ToDo`

NGINX+ with NGINX Controller
############################

:kbd:`ToDo`

