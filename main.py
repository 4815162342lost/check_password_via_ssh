#!/usr/bin/python3
import subprocess

error_servers=open("errors_server.txt", "w")
date=subprocess.Popen('date +%W%m%u', shell=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.read().rstrip()

with open("server_list.txt", "r") as servers:
        for current_server in servers.readlines():
            current_server=current_server.rstrip("\n").split(" ")[0]

            try:
                proc=subprocess.Popen("sshpass -p '2' ssh root@"+ current_server + " 'date +%W%m%u'", shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                error_servers.write("Connection issue: " + current_server +"\n")
            elif proc_err_out.find("Permission denied") != -1:
                print("Wrong password on the server " + current_server)
                error_servers.write("Wrong password: " + current_server + "\n")
            else:
                print("Another error with the server " + current_server)
                error_servers.write("Unknown error: " + current_server + "\n")
