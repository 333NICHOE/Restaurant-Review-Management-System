import server
import auth

def main ():
    
    connection = server.dbConnection()
    
    if ( connection == None ):
        return
    
    print('Connected to Database!')
    
    auth.start()
    
main()