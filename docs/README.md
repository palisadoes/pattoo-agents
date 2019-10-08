# Pattoo Agent Documentation

## Introduction

`pattoo` agents can be used to easily poll IoT data.

## Agents
Here is a description of currently supported `pattoo` agents.

| Agent | Description                    |
|--|--|
|[pattoo-os-passived](PATTOO-OS.md)| Python3 based daemon that presents `pattoo` data via a web API URL. This data can be regularly polled from a central server|
|[pattoo-os-hub](PATTOO-OS.md)| Python3 based daemon that polls `pattoo-os-passived` APIs for data. (Under development)|
|[pattoo-os-actived](PATTOO-OS.md)| Python3 based daemon that posts  `pattoo` to a central server.|

## JSON Data Format

A comprehensive description of `pattoo` JSON data [ can be found here.](DATA.md)
