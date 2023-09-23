#!/usr/bin/python3

import sys
import os
import pwd

uid = os.getuid()
entrada_usuario = pwd.getpwuid(uid)
gecos = entrada_usuario.pw_gecos
carpeta_personal = os.path.expanduser("~")
ps1 = os.environ.get('PS1')
if uid > 1000:

    print("El usuario puede ejecutar el script")
    print("El id del usuario es: ", uid)
    print("El gecos del usuario es: ", gecos)
    print("La carpeta personal del usuario es: ", carpeta_personal)
    if ps1 is not None:
        print("El valor de la variable es: ", ps1)
    else:
        print("La variable $PS1 no está definida en este entorno")
    
else:
    print("El usuario no puede ejecutar el script, no ha de ser usuario especial o administrador ")
    sys.exit(1)


