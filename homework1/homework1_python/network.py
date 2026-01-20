import socket
import json


def generate_reply_json(beam_angle, reset_flag):
    return f"""{{"beam_angle": {beam_angle},"reset_system": {"true" if reset_flag else "false"}}}"""


# Configuration
listen_ip = "127.0.0.1"
listen_port = 5005
send_ip = "127.0.0.1"
send_port = 5006

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((listen_ip, listen_port))

print(f"Python listening on {listen_port}...")
print(generate_reply_json(1, True))
while True:
    # 1. Receive data
    data, addr = sock.recvfrom(1024)
    json_str = data.decode("utf-8")
    recv_data = json.loads(json_str)
    print(f"Received from Unity: {recv_data}")

    # 2. Send reply
    reply = generate_reply_json(1, True)
    sock.sendto(reply.encode("utf-8"), (send_ip, send_port))
