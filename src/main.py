import api
import sys

def usage ():
    pass

def main ():
    argvn = len (sys.argv)

    print (sys.argv)

    # No args, usage
    if argvn < 2:
        usage ()
        sys.exit ()

    # login
    elif argvn > 1 and sys.argv[1] == 'login':
        email = None
        password = None

        if argvn > 2:
            email = sys.argv[2]
        else:
            email = input ('Email: ')
        if argvn > 3:
            password = sys.argv[3]
        else:
            password = input ('Password: ')
        
    # gps-serve
    elif argvn > 2 and sys.argv[1] == 'gps-serve':
        boat = sys.argv[2]
        port = 2947

        if argvn > 3:
            port = int (sys.argv[3])

if __name__ == "__main__":
    main ()