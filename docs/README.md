# Pattoo Agent Documentation

## Introduction

`pattoo` agents can be used to easily poll IoT data. The data is sent to a centralized `pattoo` server for processing.

## Terminology

A comprehensive list of `pattoo` terminologies [ can be found here.](GLOSSARY.md)

## Installation

The documentation in [INSTALLATION.md](INSTALLATION.md)  covers this.

## Configuration
The documentation in [CONFIGURATION.md](CONFIGURATION.md)  covers this.

## Agents
Here is a description of currently supported `pattoo` agents.

| Agent | Description                    |
|--|--|
|[pattoo-os-spoked](PATTOO-OS.md)| Python3 based daemon that presents `pattoo` data via a web API URL. This data can be regularly polled from a central server|
|[pattoo-os-hubd](PATTOO-OS.md)| Python3 based daemon that polls `pattoo-os-spoked` APIs for data. 
|[pattoo-os-autonomousd](PATTOO-OS.md)| Python3 based daemon that posts  `pattoo` to a central server.|
|[pattoo-os-snmpd](PATTOO-SNMPD.md)| Python3 based daemon that polls remote `ip_devices` for SNMP data.

## JSON Data Format

A comprehensive description of `pattoo` JSON data [ can be found here.](DATA.md)
