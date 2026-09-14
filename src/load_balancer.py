import requests
from flask import request, Response
from pathlib import Path

# variable for keeping track of index for server switching
current_server_idx = 0

# list for maintaining the server names and for load balancer logic
servers_list = []

# extract servers list
def get_servers():
    global servers_list
    current_working_directory = Path(__file__).resolve().parent
    servers_list_config = current_working_directory/"config"/"servers_list.txt"
    with open(servers_list_config) as f:
        servers_list = f.readlines()

# initially extract the servers list
get_servers()

# strategy for switching the server for request forwarding - Round Robin
def get_next_server():
    global current_server_idx
    if servers_list:
        server = servers_list[current_server_idx].strip() + "/data"
        current_server_idx = (current_server_idx + 1) % len(servers_list)
        return server
    return ""

# This will be entry point into the load balancer application
def load_balancer():
    # Pick the next backend server using Round Robin
    server = get_next_server()
    if not server:
        return "Could not retrieve server address.", 503

    try:
        resp = requests.request(
            method=request.method,
            url=server,
            timeout=5
        )
        return Response(
            response=resp.text,
            status=resp.status_code
        )
    except requests.exceptions.RequestException:
        return "Backend server unavailable.", 503