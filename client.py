import re
import email
import imaplib
import pytz
from colorama import init, Back, Fore
from datetime import datetime

#Extras
init()
utc=pytz.UTC

#Datos de Usuario
usuario=""
contrasena=""
mail_server="imap.gmail.com"

#Emails a Revisar
casilla="inbox"
direccion="noresponder@pizzapizza.cl"
regex=r"^010001[6-7]{1}[0-9a-f]{9}\-[0-9a-f]{8}(\-[0-9a-f]{4}){3}\-[0-9a-f]{12}-[0]{6}@(email|[a-z]{2}(\-gov)?\-[a-z]{4,9}\-[1-3]{1})\.amazonses\.com$"
fecharegexstring="20/07/18"
fecharegex=utc.localize(datetime.strptime(fecharegexstring,'%d/%m/%y'))

#Proceso de Login
mail=imaplib.IMAP4_SSL(mail_server)
mail.login(usuario,contrasena)
print(Back.GREEN+"Inicio de sesión correctamente realizado en cuenta "+Fore.YELLOW+usuario+Fore.RESET+"."+Back.RESET)

#Busqueda de mails
mail.select(casilla,True)
query='(FROM '+direccion+')'
check, mensajes=mail.search(None,query)
print("Buscando correos provenientes de "+Back.RED+Fore.YELLOW+direccion+Back.RESET+Fore.RESET+" en la casilla "+casilla+".")

#Receptor de Message ID's
print(Back.GREEN+"Correos encontrados. "+Fore.BLUE+"Análisis de Message ID en proceso."+Fore.RESET+Back.RESET)
identificador=mensajes[0].split()
for m in identificador:
    correos, data=mail.fetch(m,"(BODY[HEADER.FIELDS (MESSAGE-ID DATE)])")
    datos=data[0][1].decode("utf-8").split("\r\n")
    fechastring=datos[0][6:37]
    fecha=datetime.strptime(fechastring,'%a, %d %b %Y %H:%M:%S %z')
    messageid=datos[1][12:]
    messageid=messageid[1:len(messageid)-1]
    print(Fore.YELLOW+"Fecha Obtenida: "+Fore.RESET+fechastring)
    print(Fore.YELLOW+"Message ID: "+Fore.RESET+messageid)
    validador=re.search(regex,messageid)
    if(validador):
        print(Back.BLUE+"Message ID corresponde a Regex."+Back.RESET)
    else:
        if(fecharegex>fecha):
            print(Back.MAGENTA+"Message ID no corresponde a Regex. Regex creado a partir de fecha posterior a la del mail recibido."+Back.RESET)
        else:
            print(Back.RED+"Message ID no corresponde a Regex. "+Fore.YELLOW+"ALERTA, PODRÍA SER UNA SUPLANTACIÓN DE IDENTIDAD."+Fore.RESET+Back.RESET)
