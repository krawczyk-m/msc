# Master of Science dissertation

Repository contains all the necessary scripts to run diagnostics
for the Master of Science dissertatation in the field of steganography.

## Prerequisites

Required packages for node running scapy & nfqueue related scripts (suggested setup):

..* system packages: 
....* libnetfilter-queue-dev
....* libnfnetlink-dev
....* nfqueue-bindings-python
..* python-virtualenv for python package management:
....* scapy
....* NetfilterQueue

## Docker

Docker provides an easy way to add hosts for lab research. The provided Dockerfile
provisions a docker image with the network utility tools.
