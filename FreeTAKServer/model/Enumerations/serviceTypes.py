from enum import Enum

class ServiceTypes(Enum):
    TCPCOTSERVICE = "TCP-CoT-Service"
    SSLCOTSERVICE = "SSL-CoT-Service"
    TCPDPSERVICE = "TCP-DP-Service"
    SSLDPSERVICE = "TCP-DP-Service"
    APISERVICE = "API-Service"
    FEDSERVERSERVICE = "Federation-Server-Service"
    FEDCLIENTSERVICE = "Federation-Client-Service"