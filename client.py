import socket
import argparse

PORT = 1235
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=False, help='Please set the IP address of the MTDServer.')
    parser.add_argument('--port', required=False, help='Please set the Port of the MTDServer.', type=int)
    parser.add_argument('--attack', required=True, help='Please set the Attack type.')
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if args.ip:
        s.connect((str(args.ip), args.port))
    else:
        s.connect((socket.gethostname(), PORT))

    if args.attack == "recon" or args.attack == "cj":
        s.send(bytes(args.attack, "utf-8"))
        print("Attack report was sent: " + args.attack)
    else:
        print("There is no mitigation solution for this attack " + args.attack + ", please use recon or cj")


if __name__ == '__main__':
    main()