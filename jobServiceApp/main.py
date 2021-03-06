#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on july 22nd 2020

@author: quart

Important data to develop the code:

-Link to get thesis of any period ( ID changes only):     
https://sjf2.scjn.gob.mx/detalle/tesis/{ID_THESIS}

This service will add new thesis from the website

Info:
1)So it is good to start from that ID onwards
2)30 secs for every read

"""

import json
import os
import cassandraUtil as db
import utils as tool

print('Running program...')
querySt="select query,page from thesis.cjf_control where id_control=4  ALLOW FILTERING"
resultSet=db.getQuery(querySt)
lsInfo=[]
if resultSet: 
    for row in resultSet:
        lsInfo.append(str(row[0]))
        lsInfo.append(str(row[1]))
        print('Value from cassandra:',str(row[0]))
        print('Value from cassandra:',str(row[1]))
startID=int(lsInfo[1])
#The limits in readUrl may vary up to the need of the search
tool.readUrl(1,startID,5000000)  

  

