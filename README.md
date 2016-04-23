# Master of Science dissertation

Repository contains all the necessary scripts to run diagnostics
for the Master of Science dissertation in the field of steganography.

## Prerequisites

Required packages for node running scapy & nfqueue related scripts (suggested setup):

..* python-virtualenv for python package management:
....* scapy
....* NetfilterQueue (compiled from: https://github.com/kti/python-netfilterqueue - needed for set_payload)

## Docker

Docker provides an easy way to add hosts for lab research. The provided Dockerfile
provisions a docker image with the network utility tools.
