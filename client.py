import sys
import socket

from settings import SERVICES_HOST, SERVICES_PORT


class Client:
    def __init__(self):
        self.service_address = None

    def validateCPF(self, cpf):
        if self.service_address is None:
            self.lookup('validateCPF')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.service_address)
            s.sendall(cpf.encode())
            msg = s.recv(1024).decode()
        print(msg)

    def lookup(self, service: str) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVICES_HOST, SERVICES_PORT))
            s.sendall('lookup-service'.encode())
            service_connection_msg = s.recv(1024).decode()
            if 'OK' in service_connection_msg:
                s.sendall(f'{service}'.encode())
                service_address_msg = s.recv(1024).decode()
                if 'ERROR' not in service_address_msg:
                    service_host, service_port = service_address_msg.split(',')
                    self.service_address = (service_host, int(service_port))
            elif 'ERROR' in service_connection_msg:
                print(service_connection_msg)

def main():
    try:
        cpf = str(sys.argv[1])
    except:
        print('[ERROR] Missing argument: "python client.py [CPF]"')
        sys.exit(2)
    c = Client()
    c.validateCPF(cpf)

if __name__ == '__main__':
    main()
