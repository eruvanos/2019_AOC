# TCP_IP = '151.217.111.34'
from random import randint
from time import sleep

TCP_IP = '151.217.118.128'

# TCP_IP = '127.0.0.1'
TCP_PORT = 1234
from multiprocessing import Process


def main():
    import socket
    BUFFER_SIZE = 1024
    MESSAGE = "SIZE\n"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE.encode())
    data = s.recv(BUFFER_SIZE)
    print(data)
    s.close()


class Pixel(Process):
    def __init__(self) -> None:
        super().__init__()
        sleep(randint(0,100)/1000)
        import socket
        from PIL import Image

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((TCP_IP, TCP_PORT))

        im = Image.open('wir_klein.png').convert('RGB')
        _, _, w, h = im.getbbox()

        self.data = ''
        offx = 800
        offy = 50
        for x in range(w):
            for y in range(h):
                r, g, b = im.getpixel((x, y))
                self.data += self.pixel(offx + x, offy + y, r, g, b)



    def pixel(self, x, y, r, g, b, a=255):
        return f'PX {x} {y} {r:02x}{g:02x}{b:02x}\n'

    def run(self) -> None:
        data = self.data.encode()
        while True:
            self.sock.send(data)


def example():
    import socket
    from PIL import Image

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))

    def pixel(x, y, r, g, b, a=255):
        if a == 255:
            sock.send(f'PX {x} {y} {r:02x}{g:02x}{b:02x}\n'.encode())
        else:
            sock.send(f'PX {x} {y} {r:02x}{g:02x}{b:02x}{a:02x}\n'.encode())

    im = Image.open('robot.png').convert('RGBA')
    _, _, w, h = im.getbbox()

    offx = 1000
    offy = 150
    while True:
        for x in range(w):
            for y in range(h):
                r, g, b, a = im.getpixel((x, y))
                pixel(offx + x, offy + y, r, g, b, a)


def start():
    Pixel().start()


if __name__ == '__main__':
    # main()
    print(Pixel().data)

    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()
    # Pixel().start()

    # Process(target=example).start()
    # Process(target=example).start()
    # Process(target=example).start()
    # Process(target=example).start()
    # Process(target=example).start()
    # Process(target=example).start()
    # Process(target=example).start()

    # example()
