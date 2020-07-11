#!usr/bin/python3

import socket
import requests
import validators

#import ports file
from common_ports import ports_and_services


# function to validate ip or string
def validate(ipOrUrl):
    toValidate = ipOrUrl
    str = "Valid Url"
    try:
        toValidate="https://" + ipOrUrl
        request = requests.get(toValidate, stream=True, timeout=3)
    except:
        try:
            toValidate="http://" + ipOrUrl
            request = requests.get(toValidate, stream=True, timeout=3)
        except:
            str="Error: Invalid hostname"
            if not(validators.ip_address.ipv4(ipOrUrl)):
                subIP=ipOrUrl.split(".")
                count=0
                for i in subIP:
                    if i.isdigit():
                        count=count+1
                if count==4:
                    str="Error: Invalid IP address"
            else:
                str="Valid IP"
    # print(str)
    return str


def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    validity = validate(target)
    if validity!="Valid Url" and validity!="Valid IP":
        return validity
    
    host = socket.gethostbyname(target)
    # print(host)
    for port in range(port_range[0],port_range[1]+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        # print(port)
        if not(sock.connect_ex((host, port))):
            # print("Success")
            open_ports.append(port)
        sock.close()
    #if verbose is true
    if verbose==True:
        result="Open ports for "+target+" ("+host+")"+"\nPORT     SERVICE"
        for p in open_ports:
            if p<100:
                result=result+"\n"+str(p)+"       "+ports_and_services[p]
            elif p<1000:
                result=result+"\n"+str(p)+"      "+ports_and_services[p]
            else:
                result=result+"\n"+str(p)+"     "+ports_and_services[p]
        return result

    return(open_ports)

# print(get_open_ports("scanme.nmap.org", [20, 80], True))