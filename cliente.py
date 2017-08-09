import socket
import threading

def recibirMensajes():
    """ 
    FUNCION QUE CORRE EN UN HILO DIFERENTE Y QUE VALIDA SI EL SERVIDOR HA
    ENVIADO ALGUN MENSAJE
    """
    while True:
        #SE QUEDA DETENIDO HASTA QUE RECIBE UN MENSAJE
        respuesta = cliente.recv(4096)
        #SI ES VALIDO EL MENSAJE LO IMPRIMIMOS
        if respuesta:
            print("\rAlguien dijo: ", respuesta.decode("utf-8"))
            print("What's your msg? ", sep=' ', end='', flush=True)
       

#DATOS PARA CONECTARNOS AL SERVIDOR
servidor = "10.27.112.67"
puerto = 5555

#ABRIMOS CONEXION AL SERVIDOR
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((servidor, puerto))

#EJECUTAMOS LA FUNCION recibirMensajes EN UN HILO DIFERENTE AL DE LA APLICACION
hilo = threading.Thread(target=recibirMensajes)  
hilo.start()

#CICLO INFINITO QUE ENVIA LOS MENSAJES AL SERVIDOR
while True:
    #LA APLICACION ESPERA HASTA QUE EL CLIENTE CAPTURA UN DATO
    msg = input("What's your msg? ")    
    #EL MENSAJE LO ENVIA CODIFICADO EN UTF-8
    cliente.send(msg.encode('utf-8')) 

