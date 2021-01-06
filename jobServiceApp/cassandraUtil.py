import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
from InternalControl import cInternalControl

objControl= cInternalControl()


def getCluster():
    #Connect to Cassandra
    objCC=CassandraConnection()
    if objControl.heroku:
        cloud_config= {
        'secure_connect_bundle': objControl.rutaHeroku+'/secure-connect-dbquart.zip'
        }
    else:    
        cloud_config= {
        'secure_connect_bundle':objControl.rutaLocal+'secure-connect-dbquart.zip'
          }

    auth_provider = PlainTextAuthProvider(objCC.cc_user,objCC.cc_pwd)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)

    return cluster
  



def executeNonQuery(query):

    cluster=getCluster()
    session = cluster.connect()
    session.default_timeout=70
    future = session.execute_async(query)
    future.result()
                         
    return True
   
def getQuery(query):

    cluster=getCluster()
    session = cluster.connect()
    session.default_timeout=70         
    future = session.execute_async(query)
    resultSet=future.result()
    cluster.shutdown()
                                           
    return resultSet    
          
def insertJSON(json_thesis):

    cluster=getCluster()
    session = cluster.connect()
    session.default_timeout=70           
    #Insert Data as JSON
    json_thesis=json.dumps(json_thesis)
    #wf.appendInfoToFile(dirquarttest,str(idThesis)+'.json', json_thesis)                
    insertSt="INSERT INTO thesis.tbthesis JSON '"+json_thesis+"';" 
    future = session.execute_async(insertSt)
    future.result()  
    cluster.shutdown()     
                    
                         
    return True


class CassandraConnection():
    cc_user='quartadmin'
    cc_pwd='P@ssw0rd33'