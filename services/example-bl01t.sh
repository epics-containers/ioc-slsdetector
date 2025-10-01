#!/bin/bash

# A launcher for the ioc-adsimdetector-demo IOC

# prefer docker but use podman if USE_PODMAN is set
if docker version &> /dev/null && [[ -z $USE_PODMAN ]]
    then docker=docker
    else docker=podman
fi
echo "Using $docker to launch the IOC"

CA1=${EPICS_CA_SERVER_PORT:-5064}
CA2=${EPICS_CA_REPEATER_PORT:-5065}
PVA1=${EPICS_PVA_SERVER_PORT:-5075}
PVA2=${EPICS_PVA_BROADCAST_PORT:-5076}

args="--rm -it"
ca="-p 127.0.0.1:$CA1:$CA1/udp -p 127.0.0.1:$CA1-$CA2:$CA1-$CA2"
# pva="-p $PVA2:$PVA2/udp -p $PVA1-$PVA2:$PVA1-$PVA2"
image="ghcr.io/epics-containers/ioc-adsimdetector-demo:2024.11.1"
$docker run $args $ca $pva $image
