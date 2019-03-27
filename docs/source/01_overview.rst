Overview
========

CyDER is a modular and scalable tool for power system planning and operation that is interoperable with utility software, data streams, and controls.

The complexity of distribution grids is drastically increasing as a result of integrating larger shares of distributed generation and storage devices, uncertainties in renewable power generation, and advanced electronics-based controllers (Hadjsaid and Sabonnadiere 2012 Hadjsaid, Nouredine, and Jean-Claude Sabonnadiere. 2012. “Smart Power Grids.” ISBN 978-1-84821-261-9).

This necessitate a modular, extensible, and scalable power system planning tool. Such a tool should enable the coupling of different software modules that model various components of distribution system layer.

The co-simulation of independent simulators on a common platform enable specialized software and third-party tools to be leveraged to study complex interdependencies between systems while preserving simplicity, transparency, flexibility, and scalability of the simulation environment (Chatzivasileiadis et al. 2016 Chatzivasileiadis, Spyros, Marco Bonvini, Javier Matanza, Rongxin Yin, Zhenhua Liu, Thierry Nouidui, Emre C. Kara, et al. 2016. “Cyber–Physical Modeling of Distributed Resources for Distribution System Operations.” Proceedings of the IEEE 104 (4): 789–806. doi: 10.1109/JPROC.2016.2520738).

The goal of the CyDER platform is to use a well-defined open industry standard to couple power system tools in different time domains and voltage levels, such as quasi-static distribution and transmission system simulations, and real-time digital simulations, with tools that are not developed within the traditional scope of power systems (e.g. buildings, electric vehicles).

CyDER leverages the FMI standard to seamlessly integrate different software modules in a using a standardized API with a well-defined semantics.
