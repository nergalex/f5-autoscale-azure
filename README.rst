F5 autoscaling in Microsoft Azure
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
The Edge Security design described bellow is an example. The methodology is described in this [webinar](https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fevent.on24.com%2Finterface%2Fregistration%2Fautoreg%2Findex.html%3Feventid%3D2209631%26sessionid%3D1%26key%3D3D42A4051EE862113709FEF2AFA82733%26firstname%3Darnaud%26lastname%3Dlemaire%26email%3Da.lemaire%40f5.com%26job_title%3DMngr%252C%2BSystems%2Bengineering%26company%3DF5%2BNetworks%2BInc.%26country%3DNetherlands%26zip%3D3528%2BBJ%26work_phone%3D202014940&data=02%7C01%7Cyoucef.hamou%40external.total.com%7C23f9a37a57b14e0aa6cf08d7d63ce224%7C329e91b0e21f48fba071456717ecc28e%7C1%7C0%7C637213429317758799&sdata=Q7nFwvlTtkC1C43OoKcKuZy0x2Od8e22IRjsRNy%2BWfE%3D&reserved=0)

Demo
###############
- Deploy an Application

[![demo](http://img.youtube.com/vi/x4CnlKm_Ik8/0.jpg)](http://www.youtube.com/watch?v=x4CnlKm_Ik8)







