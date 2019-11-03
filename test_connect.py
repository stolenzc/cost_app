import socket


def net_is_used(ip='127.0.0.1',port=3306):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,port))
        s.shutdown(2)
        print('%s:%d is used' % (ip,port))
        return True
    except:
        print('%s:%d is unused' % (ip,port))
        return False


print(net_is_used('192.168.0.29'))