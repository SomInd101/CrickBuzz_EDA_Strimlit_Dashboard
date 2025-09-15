import mysql.connector as My_conn
db_var="Crick_biz"

class sql_oper:
    def __init__(self, user, password, host, port, allow_local_infile):
        # self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.allow_local_infile= allow_local_infile
    def db_creation(self):
        db_cont=My_conn.connect(user= self.user,
                                password = self.password,
                                host = self.host,
                                port = self.port
        )
        db_query=f'''CREATE DATABASE IF NOT EXISTS {db_var}'''
        cursor = db_cont.cursor()
        cursor.execute(db_query)
        db_cont.commit()
        db_cont.close()
        cursor.close()
        return db_var

    def connection_myAdmin(self ):
        cont_myd =  My_conn.connect(database = self.db_creation(), 
                                      user= self.user, 
                                      password = self.password, 
                                      host = self.host, 
                                      port = self.port,
                                      allow_local_infile=self.allow_local_infile
                                      )
        cur_agAdm = cont_myd.cursor()
        return cont_myd, cur_agAdm

#connection for pulling data from PERTICUALER DATABASE tables
class db_puller():
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        # self.allow_local_infile= allow_local_infile

    def connection_myAdminP(self ):
        connect_puller =  My_conn.connect(database = self.database, 
                                        user= self.user, 
                                        password = self.password, 
                                        host = self.host, 
                                        port = self.port
                                        #,allow_local_infile=self.allow_local_infile
                                        )
        cur_puller_Adm = connect_puller.cursor()
        return connect_puller, cur_puller_Adm

        
 
# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\cb_sql_conn.py