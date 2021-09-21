  Intro
  -----

  MilkyWay is a Python library for efficient creation of OPC-UA servers. MilkyWay is strongly
  related to the quasar ecosystem by:
  * profiting from the quasar notation (by the means of loading the quasar design files)
  * using similar architectural concepts (e.g handling data representation concerns invisibly to the programmer)
  * using same configuration schema for configuration files as the ordinary quasar-based OPC-UA servers
  * letting profit from the other elements of the ecosystem such as UaObjects or WinCC OA integration

  MilkyWay is a pure Python development. Currently it uses the "opcua" (see PyPi) as the OPCUA provider.

  MilkyWay is especially attractive for transition of existing quasar-based projects from C++ to Python, as well as for all new Python OPC-UA projects in which the benefits of staying in the quasar ecosystem (e.g. UaObjects or Cacophony) are expected.


  Basic tutorial
  --------------

  To run a MilkyWay-powered OPC-UA server, one needs:
  
