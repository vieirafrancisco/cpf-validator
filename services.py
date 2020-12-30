import sys
import socket

from cpf import validate
from settings import SERVICES_HOST, SERVICES_PORT

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @property
    def address(self):
        return (self.host, int(self.port))

    def listen(self):
        pass


class ValidateCPFServer(Server):
    def __init__(self, host='127.0.0.1', port=65433):
        super().__init__(host, port)
        self.binded = False

    def bind(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVICES_HOST, SERVICES_PORT))
            s.sendall('bind-service'.encode())
            service_connection_msg = s.recv(1024).decode()
            if service_connection_msg.split(':')[0] == 'OK':
                s.sendall(f'validateCPF,{self.host},{self.port}'.encode())
                msg = s.recv(1024).decode()
                print(f'Bind service: "{msg}"')
            elif service_connection_msg.split(':')[0] == 'ERROR':
                print(service_connection_msg)

    def listen(self):
        if not self.binded:
            self.bind()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.address)
            print(f'{self} listening on port {self.port}')
            while True:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        if validate(data):
                            conn.sendall('cpf válido!'.encode())
                        else:
                            conn.sendall('cpf inválido!'.encode())


class ServiceServer(Server):
    def __init__(self, host=SERVICES_HOST, port=SERVICES_PORT):
        super().__init__(host, port)
        self.services = dict()

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.address)
            print(f'{self} listening on port {self.port}')
            while True:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        protocol = conn.recv(1024)
                        if not protocol:
                            break
                        if protocol.decode() == 'bind-service':
                            conn.sendall('OK: correct service name!'.encode())
                            data = conn.recv(1024)
                            service_name, host, port = data.decode().split(',')
                            self.bind(service_name, host, port)
                            conn.sendall('success'.encode())
                        elif protocol.decode() == 'lookup-service':
                            conn.sendall('OK: sendme the service-name'.encode())
                            service_name = conn.recv(1024).decode()
                            try:
                                service_addess = self.lookup(service_name)
                                print(service_addess)
                                conn.sendall(f'{service_addess[0]},{service_addess[1]}'.encode())
                            except Exception:
                                conn.sendall('ERROR: invalid service name!'.encode())
                        else:
                            conn.sendall('ERROR: invalid service name!'.encode())

    def bind(self, service: str, host: str, port: str) -> None:
        self.services[service] = (host, int(port))

    def lookup(self, service):
        return self.services[service]

def main():
    try:
        arg = sys.argv[1]
    except Exception:
        print('[ERROR] Missing argument: "python services.py [SERVICE_NAME]"')
        sys.exit(2)
    if arg == 'cpf-validator-server':
        vc = ValidateCPFServer()
        vc.listen()
    elif arg == 'main-server':
        s = ServiceServer()
        s.listen()

if __name__ == '__main__':
    main()
