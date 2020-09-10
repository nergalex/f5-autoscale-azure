Autoscale F5 products in Microsoft Azure
==================================================

.. contents:: Table of Contents

Summary
###############
Use Case
*********************
- **Cost** -- securise access to your applications by centralizing Security features in an Edge Security infrastructure
- **Security** -- use adaptative security features - editor agnostic - depending on the criticality of your assets (Defense in Depth methodology)
- **Multi-tenancy** -- manage and monitor each Application individually like a dedicated infrastructure (RBAC feature)
- **Resiliency** -- deploy Applications in Multi-regions and/or Multi-clouds by automating deployment of your infrastructure as a replicate
- **Reliability** -- deploy Applications using Canary or A/B testing on your infrastructure replicate (GSLB feature)
- **Dynamism** -- update configuration based on upstream server life cycle by using Service Discovery feature at Edge

Benefit
*********************
- **Cost** -- maximize CPU consumption of Security assets
- **unlock Security** -- be free to use and change Security feature products in data path at Edge, transparently for Application owners
- **Multi-tenancy** -- offer an Edge Security as a managed service for Application development team and hide infrastructure management owned by for DevSecOps team
- **Resiliency** -- deploy on specific Edge replicates depending on the Service Level Objective of each Application (end-user latency, availability...)
- **Reliability** -- prevent CPU and upstream port exhaustion by setting CPU and outbound flows as a metric in scaling policy
- **Observability** -- deploy Edge Security replicate in closest regions of your end-users and monitor metrics and security events for global visibility

Architecture
*********************
The Edge Security architecture described in this article is a solution based on specific customer needs, business expectation and security requirements.
There is no unique solution, please follow the methodology presented in the Secure Cloud Architecture webinar, available in
`English <https://gateway.on24.com/wcc/eh/1140560/lp/2200026/f5-emea-webinar-march-2020-english>`_,
`French <https://gateway.on24.com/wcc/eh/1140560/lp/2209631/f5-emea-webinar-march-2020-french>`_
or other `languages  <https://www.f5.com/c/emea-2020/emea-webinar-library>`_.
Feel free to reach `F5 people <https://www.linkedin.com/company/f5/people/>`_ for a dedicated workshop.

.. figure:: _figure/Architecture_INBOUND.png

Design Consideration
*********************
Ths article is to propose a solution based on:
- native cloud provider autoscaling feature
- F5 Controller products for Out Of Band management and Analytics
- customer eco-system products

For autoscale need in a another customer context,
`ARM templates <https://github.com/F5Networks/f5-azure-arm-templates>`_ - supported by F5 - could be sufficient.

Automation tool used here is Ansible. F5 products can also be deployed with Terraform, please refer to those good `articles written by Jeff Giroux <https://github.com/JeffGiroux/f5_terraform>`_

Demo
###############
- Automate an Application deployment
.. raw:: html

    <a href="http://www.youtube.com/watch?v=p1rfhssaE_U"><img src="http://img.youtube.com/vi/p1rfhssaE_U/0.jpg" width="200" height="200" title="Automate an Application deployment" alt="Automate an Application deployment"></a>

- Scale Out VMSS NGINX+ managed by NGINX Controller
.. raw:: html

    <a href="http://www.youtube.com/watch?v=x4CnlKm_Ik8"><img src="http://img.youtube.com/vi/x4CnlKm_Ik8/0.jpg" width="200" height="200" title="Scale Out VMSS NGINX+ managed by NGINX Controller" alt="Scale Out VMSS NGINX+ managed by NGINX Controller"></a>

- Scale In VMSS NGINX+ managed by NGINX Controller
.. raw:: html

    <a href="http://www.youtube.com/watch?v=8tG1QF0Rurw"><img src="http://img.youtube.com/vi/8tG1QF0Rurw/0.jpg" width="200" height="200" title="Scale In VMSS NGINX+ managed by NGINX Controller" alt="Scale In VMSS NGINX+ managed by NGINX Controller"></a>

- Scale Out VMSS BIG-IP managed by BIG-IQ
.. raw:: html

    <a href="http://www.youtube.com/watch?v=EvSrmwhDP2o"><img src="http://img.youtube.com/vi/EvSrmwhDP2o/0.jpg" width="200" height="200" title="Scale Out VMSS BIG-IP managed by BIG-IQ" alt="Scale Out VMSS BIG-IP managed by BIG-IQ"></a>

- Scale Out VMSS BIG-IP managed by BIG-IQ
.. raw:: html

    <a href="http://www.youtube.com/watch?v=-zzKjA_mFIY"><img src="http://img.youtube.com/vi/-zzKjA_mFIY/0.jpg" width="200" height="200" title="Scale In VMSS BIG-IP managed by BIG-IQ" alt="Scale In VMSS BIG-IP managed by BIG-IQ"></a>




