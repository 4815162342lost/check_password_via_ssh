#!/usr/bin/python3
import subprocess
import re

error_servers=open("errors_server.txt", "w")
date=subprocess.Popen('date +%W%m%Y', shell=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.read().rstrip()

with open("server_list.txt", "r") as servers:
        for current_server in servers.readlines():
            current_server=current_server.rstrip("\n")
            split_ip_from_name=re.split(" +", current_server)
            current_server = split_ip_from_name[0]
            host_name = split_ip_from_name[1]

            try:
                proc=subprocess.Popen("sshpass -p '1' ssh  -o 'StrictHostKeyChecking no' root@"+ current_server + " 'date +%W%m%Y'", shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                proc.wait(timeout=60)
            except:
                print("Timeout error with server  " + current_server)
            proc_out=proc.stdout.read()
            proc_err_out=proc.stderr.read()

            if proc_out.find(date) != -1:
                print("All OK with server " + current_server)
                continue
            elif proc_err_out.find("No route to host") != -1:
                print("Connection failed with the server " + current_server)
                error_servers.write("Connection issue: " + current_server + " " + host_name + "\n")
            elif proc_err_out.find("Permission denied") != -1:
                print("Wrong password on the server " + current_server)
                error_servers.write("Wrong password: " + current_server  + " " + host_name + "\n")
            elif proc_err_out.find("Received disconnect") != -1:
                print("Server refused our connection " + current_server)
                error_servers.write("Client Disconnect: " + current_server  + " " + host_name + "\n")
            else:
                print("Another error with the server " + current_server)
                error_servers.write("Unknown error: " + current_server  + " " + host_name + "\n")
