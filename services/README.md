# IOC Instance bl01t-ea-ioc-02

This services folder contains an example simple IOC. The IOC is baked into an additional container image target for this project and can therefore be run directly as follows:

```bash
./services/example-bl01t.sh

export EPICS_CA_ADDR_LIST=127.0.0.1
caget caget BL01T-EA-TST-02:UPTIME
```

It can be run from inside the developer container as well:

```bash
cd /epics/ioc
make
ibek dev instance /workspaces/ioc-adsimdetector/services/bl01t-ea-ioc-02/
./start.sh
```

Finally there is an example GUI provided that can be launched from outside the container:

```bash
./opi/phoebus-launch.sh
```
