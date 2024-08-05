# 2024IntershipRainfallMonitoring

This github repository is the result of an internship made by 2 student from Polytech Nice Sophia at DNIIT (Danang International Institute of Technology).

The main goal of this internship is the creation of a **rainfall monitoring and alerting system**.

## Table of Contents
- [State of the project](#state-of-the-project)
- [Components](#components)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Usage](#usage)
- [Authors](#authors)

## State of the project

Currently, we have a rain gauge and a water level sensor who are able to send their data to the LoRaWan Gateway of DNIIT. 

We had encountered a few issues with these sensors :
- The water level sensor is faulty, the measurement it give are false.
- The rain gauge is not accurate enough to measure small quantity of rain, to trigger it we needed to pour a lot of water into it. But the other measurement it does are correct.

These data are then transfered to an MQTT queue. These queue are consumed by our node-red docker image that scrap all the data from the messages and expose them to the /metrics endpoint of node-red for it to be scrapped by our prometheus container. It then serve as a datasource for our grafana dashboard.

Since it was required by our tutor to have dynamic threshold that can be modified at any moment by the consumer of these service, we used a node-exporter container to expose the value of the threshold to prometheus also. Node exporter take the value he expose from a text file that can be modified with the python script named **update_threshold.py** located in the folder with the docker images.

These threshold are used in the alerting system set in grafana and are currently arbitrary values since no values were given by our tutor. The alerting send email but since no mailing service was provided we used a free one [mailgun](http://app.mailgun.com). The credentials of the mailgun account will not be given in this github repository since it's a personal account, but a sample .env.exemple file will be provided for the user of this repo to create the appropriate .env file.

Once the .env file set correctly, the alerting should work fine also.

## Components

For this project we were given the following elements :
- A rain gauge sensor
- A water level sensor
- An UCA Board

## Repository Structure

This github repository contains currently 2 main parts :
- A folder with the Arduino code for the sensors named **arduino**
- A folder with the docker image and compose to run on the server named **server**

The arduino folder contain a folder with the libraries and one with the actual code. The libraries are to copy paste in your Arduino/libraries folder to run the code locally.

The server folder contain every file needed to run the grafana/prometheus/node-red/node-exporter stack, but to use the alerting on grafana you'll need to create a .env file similar to the .env.example provided but with the credentials of the mailgun account.

## Requirements

For the arduino part, you can follow the guide here :
https://github.com/FabienFerrero/UCA21/tree/main

This guide was made by a teacher from UCA and also contains sample of LoRaWan arduino code used as a base in this project.

<br/>

For the docker part you need :
- A working installation of docker to launch the container
- An installation of python 3, we used python 3.10.12 for our development initally
- An account on mailgun for the credentials used in the .env file

If you want to deploy the container on the server of DNIIT you'll need to follow their tutorial on OpenVPN and an access to their virtual machine.

## Usage

### Arduino

For this part here is the documentation containing the code, the wiring, and the sensor details for the water level sensor : 
https://wiki.dfrobot.com/Throw-in_Type_Liquid_Level_Transmitter_SKU_KIT0139

For the rain gauge everything was handled by our vietnamese colleague so we don't possess the wiring or the code used.

The code we use for the water level do the measurement as explained in the code of the documentation and then use the code from UCA board for LoRaWan to send all data on the gateway.

### Server

To launch everything, just do `docker compose up` or if you don't want to see the logs `docker compose up -d` and then you'll have deployed :
- grafana on port 3000
- prometheus on port 9090
- node-red on port 1880
- node-exporter on port 9100

To modify the threshold for the alerting do `./update_threshold.py` or `python3 update_threshold.py` and then insert the new values for the threshold. To add new one you'll need to modify the python script but it's a simple one. The values are in the file server/node-exporter/initial_value.prom.

## Authors

This work was solely done by :
- Axel DELILLE ([Tsukoyachi](https://github.com/Tsukoyachi) on GitHub)
- Loïc PALAYER ([low-hic](https://github.com/low-hik) on GitHub)

We were under the supervision of M. Van Lic Tran from DNIIT.

