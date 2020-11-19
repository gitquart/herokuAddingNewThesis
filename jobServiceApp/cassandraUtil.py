import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
pathtohere=os.getcwd()

def updatePage(page):

    #Connect to Cassandra
    objCC=CassandraConnection()
    cloud_config= {
        'secure_connect_bundle': pathtohere+'/jobServiceApp/secure-connect-dbquart.zip'
    }
    
    auth_provider = PlainTextAuthProvider(objCC.cc_user,objCC.cc_pwd)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    session.default_timeout=70
    page=str(page)
    querySt="update thesis.cjf_control set page="+page+" where  id_control=4;"          
    future = session.execute_async(querySt)
    future.result()
                         
    return True
   
def getPageAndTopic():

    #Connect to Cassandra
    objCC=CassandraConnection()
    cloud_config= {
        'secure_connect_bundle': pathtohere+'/jobServiceApp/secure-connect-dbquart.zip'
    }
    
    auth_provider = PlainTextAuthProvider(objCC.cc_user,objCC.cc_pwd)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    session.default_timeout=70
    row=''
    querySt="select query,page from thesis.cjf_control where id_control=4  ALLOW FILTERING"
                
    future = session.execute_async(querySt)
    row=future.result()
    lsInfo=[]
        
    if row: 
        for val in row:
            lsInfo.append(str(val[0]))
            lsInfo.append(str(val[1]))
            print('Value from cassandra:',str(val[0]))
            print('Value from cassandra:',str(val[1]))
        cluster.shutdown()
                                           
    return lsInfo    
          
def cassandraBDProcess(json_thesis):
    
    global thesis_added
    global row

    #Connect to Cassandra
    objCC=CassandraConnection()
    cloud_config= {

        'secure_connect_bundle': pathtohere+'/jobServiceApp/secure-connect-dbquart.zip'
         
    }
    
   
    auth_provider = PlainTextAuthProvider(objCC.cc_user,objCC.cc_pwd)
    #Get values for query
    #Ejemplo : Décima Época
    thesis_added=False
    
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    session.default_timeout=70
    row=''
    idThesis=json_thesis['id_thesis']
    heading=json_thesis['heading']
    #Check wheter or not the record exists
           
    querySt="select id_thesis from thesis.tbthesis where id_thesis="+str(idThesis)+" and heading='"+heading+"'"
                
    future = session.execute_async(querySt)
    row=future.result()
        
    if row: 
        thesis_added=False
        cluster.shutdown()
    else:
        #Insert Data as JSON
        json_thesis=json.dumps(json_thesis)
        #wf.appendInfoToFile(dirquarttest,str(idThesis)+'.json', json_thesis)                
        insertSt="INSERT INTO thesis.tbthesis JSON '"+json_thesis+"';" 
        future = session.execute_async(insertSt)
        future.result()  
        thesis_added=True
        cluster.shutdown()     
                    
                         
    return thesis_added


class CassandraConnection():
    cc_user='quartadmin'
    cc_pwd='P@ssw0rd33'