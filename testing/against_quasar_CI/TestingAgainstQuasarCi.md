Intro
===

Preface
---

MilkyWay belongs to the quasar ecosystem. The primary common part is the adherence to
Design files in the quasar format. In addition it is expected that quasar servers config files (i.e. where OPCUA instances are listed, typically called "config.xml") will natively
be loaded by MilkyWay.

quasar itself has got a test suite which validates it against many defined use-cases.
The test suits has a common routine (per every defined test scenario):
* deploy the Design,
* deploy the configuration,
* deploy custom device logic (if needed),
* build the server,
* run the server,
* use UaSwissArmyKnife to connect to the server and dump its address-space as a nodeset
* validate the nodeset against the reference.

Therefore, for most tests, it is expected that one could perform the same steps (without deploying the custom device logic, as the programming language is different).

MilkyWay is expected (one day...) to produce the same address-space and expose the same behaviour like quasar for identical Design and configuration files.

How to use this suite?
---
