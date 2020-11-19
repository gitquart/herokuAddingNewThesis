#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on july 22nd 2020

@author: quart

Important data to develop the code:

-Link to get thesis of any period ( ID changes only):     
https://sjf.scjn.gob.mx/SJFSist/Paginas/DetalleGeneralV2.aspx?ID=#&Clase=DetalleTesisBL&Semanario=0

This service will add new thesis from the website

Info:
1)The last thesis in database for 10th period is 2,021,818
2)So it is good to start from that ID onwards
3)30 secs for every read

"""

import json
import os
import cassandra as db
import utils as tool
#import writeFile as wf

#Global variables


pathtohere=os.getcwd()



def main():
    print('Running program...')
    lsInfo=db.getPageAndTopic()
    startID=int(lsInfo[1])
    #The limits in readUrl may vary up to the need of the search
    tool.readUrl(1,startID,2500000)  
    print("Main program is done")
  

        
if __name__=='__main__':
    main()        
