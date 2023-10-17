#!/usr/bin/python3

import sys
import os
import subprocess

root = os.getuid()

if root != 0:
    print("necesitas tener privilegios de root para el script")
    sys.exit(1)

paquete = "itaca"

dpkg = subprocess.check_output(["dpkg","-l"], universal_newlines=True)

if paquete in dpkg:
    print("El paquete esta instalado")
    respuesta = input("Desea continuar? (s/n): ")
    if respuesta == "s":
        respuesta2 = input("Desea actualizar o reinstalar el paquete? (a/r): ")
        if respuesta2 == "a":
            subprocess.check_output(["apt","update"], universal_newlines=True)
            subprocess.check_output(["apt","upgrade", paquete], universal_newlines=True)
            print("El paquete se ha actualizado")
            sys.exit(0)
        if respuesta2 == "r":
            subprocess.check_output(["apt","install","--reinstall", paquete], universal_newlines=True)
            print("El paquete se ha reinstalado")

    if respuesta == "n":
        print("Saliendo...")
        sys.exit(0)
else:
    respuesta3 = input("El paquete no esta instalado, Quieres que obtengamos el paquete y lo instalemos? (s/n): ")
    if respuesta3 == "s":
        ruta_tmp = "/tmp/"
        gz = "Packages.gz"
        package = ruta_tmp + gz
        mirror_url = "http://lliurex.net"
        distro = "focal"
        packages_gz_file=mirror_url+"/"+distro+"/dists/focal-updates/main/binary-amd64/Packages.gz"

        subprocess.check_output(["wget","-P", ruta_tmp, packages_gz_file], universal_newlines=True)
        subprocess.check_output(["gzip","-d", package], universal_newlines=True)

        fichero = "Packages"
        ruta_package = ruta_tmp + fichero
        ruta_itaca = "pool/main/i"

        f = open(ruta_package,"r")

        for linea in f:
            if linea.startswith("Filename:") and ruta_itaca in linea and "itaca" in linea:
                ruta_itaca = linea.split()[1]
                deb = linea.split()[4]
        f.close()

        descargar_deb = mirror_url+"/"+distro+"/"+ruta_itaca
        ruta_descargas = "~/Descargas"
        ruta_deb = ruta_descargas+"/"+deb

        subprocess.check_output(["wget","-P", ruta_descargas, descargar_deb], universal_newlines=True)
        subprocess.check_output(["dpkg","-i", ruta_deb], universal_newlines=True)
        print("El paquete se ha instalado")
