import socket
import threading

def conexiones(socket_cliente):    
    """
        CADA CLIENTE QUE SE CONECTA SE VA A ESTAR VALIDANDO SI ENVIA UN NUEVO MENSAJE
        SI UN CLIENTE ENVIO UN MENSAJE, ENTONCES ESE MENSAJE SE REENVIA
        A TODOS LOS DEMAS CLIENTES MENOS A EL MISMO
        SE UTILIZA UN HILO PARA CADA CLIENTE QUE SE CONECTA
    """
    try:
        #CICLO INFINITO HASTA QUE UN CLIENTE SE DESCONECTA
        while True:      
            #ESTA INSTRUCCION DETIENE LA EJECUCION DEL HILO HASTA QUE RECIBA UN MENSAJE      
            peticion = socket_cliente.recv(1024)
            #SI RECIBIO UNA PETICION CONTINUA, PERO VALIDA QUE NO SEA NULA
            if peticion:
                #SERVIDOR IMPRIME EL MENSAJE QUE ENVIO EL CLIENTE
                print("[*] Mensaje recibido:", peticion)

                #si se envia una cadena se tiene que codificar en ascii
                #socket_cliente.send("recibido".encode('ascii')) 

                #SE RECORRE EL LISTADO DE CLIENTES
                for i in listaClientes:
                    #SE VALIDA QUE EL CLIENTE ITERADO NO SEA IGUAL AL DEL MISMO HILO
                    if socket_cliente!=i:
                        #SE ENVIA EL MENSAJE AL CLIENTE ITERADO
                        i.send(peticion)             
    except:        
        print("Alguien salio!")
        #CUANDO CLIENTE SALE SE ELIMINA DE LA LISTA
        listaClientes.remove(socket_cliente)          
          

#DATOS DEL SERVIDOR PARA QUE UN CLIENTE PUEDA CONECTARSE
ip = "10.27.112.67"
puerto = 5555
max_conexiones = 5
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#INICIA EL SERVIDOR
servidor.bind((ip, puerto))
servidor.listen(max_conexiones)

#MENSAJE PARA AVISAR QUE CLIENTE YA ESTA ESPERANDO CONEXIONES
print("[*] Esperando conexiones en %s:%d" % (ip, puerto))

#LISTA DE LOS HILOS DE CADA CLIENTE Y DEL OBJETO SOCKET DEL CLIENTE
listaConexiones = []
listaClientes = []

#CICLO INFINITO DEL SERVIDOR EN EL SE VALIDA LAS CONEXIONES ENTRANTES
#Y POR CADA CONEXION ENTRANTE SE CREA UN HILO PARA QUE SE ESTE VALIDANDO
#SI EL CLIENTE ENVIA MENSAJES Y RENVIARSELOS A TODOS QUE ESTAN EN LA LISTA DE CLIENTES
while True:
    #ACEPTA UNA NUEVA CONEXION DE UN CLIENTE
    cliente, direccion = servidor.accept()
    print("[*] Conexion establecida con %s:%d" % (direccion[0], direccion[1]))

    #AGREGA A LA LISTA CLIENTES EL OBJETO SOCKET ENTRANTE
    listaClientes.append(cliente)
    #AGREGA A LA LISTA CONEXIONES UN NUEVO HILO
    listaConexiones.append(threading.Thread(target=conexiones, args=(cliente,)))  
    #INICIA A EJECUTAR EL HILO EL ULTIMO ELEMENTO DE LA LISTA DE HILOS  
    listaConexiones[-1].start()