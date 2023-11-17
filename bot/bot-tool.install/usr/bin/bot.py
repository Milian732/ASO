#!/usr/bin/python3

# pylint: disable=unused-argument

# This program is dedicated to the public domain under the CC0 license.


"""

Simple Bot to reply to Telegram messages.


First, a few handler functions are defined. Then, those functions are passed to

the Application and registered at their respective places.

Then, the bot is started and runs until we press Ctrl-C on the command line.


Usage:

Basic Echobot example, repeats messages.

Press Ctrl-C on the command line or send a signal to the process to stop the

bot.

"""


import logging
import sys
import netifaces
import subprocess
import psutil
import nmap
import re

from telegram import ForceReply, Update

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


# Enable logging

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

# set higher logging level for httpx to avoid all GET and POST requests being logged

logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and

# context.

contador_info = 0
contador_host_info = 0
contador_net_info = 0
contador_ping = 0
contador_errorlog = 0
contador_estado_servicio = 0
contador_arrancar_servicio = 0
contador_apagar_servicio = 0
contador_puertos = 0
contador_nmap = 0

async def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	global contador_info, contador_host_info, contador_net_info, contador_ping, contador_errorlog, contador_estado_servicio, contador_arrancar_servicio, contador_apagar_servicio, contador_puertos, contador_nmap

	total_comandos = contador_info+contador_host_info+contador_net_info+contador_ping+contador_errorlog+contador_estado_servicio+contador_arrancar_servicio+contador_apagar_servicio+contador_puertos+contador_nmap

	porcentaje_info = (contador_info / total_comandos * 100) if total_comandos > 0 else 0
	porcentaje_host_info = (contador_host_info / total_comandos * 100) if total_comandos > 0 else 0
	porcentaje_net_info = (contador_net_info / total_comandos * 100) if total_comandos > 0 else 0
	porcentaje_ping = (contador_ping / total_comandos * 100) if total_comandos > 0 else 0
	porcentaje_errorlog = (contador_errorlog / total_comandos * 100) if total_comandos > 0 else 0
	porcentaje_estado_servicio = (contador_estado_servicio / total_comandos * 100) if total_comandos > 0 else 0
	porcentaje_arrancar_servicio = (contador_arrancar_servicio / total_comandos * 100) if total_comandos > 0 else 0
	porcentaje_apagar_servicio = (contador_apagar_servicio / total_comandos * 100) if total_comandos > 0 else 0
	porcentaje_puertos = (contador_puertos / total_comandos * 100) if total_comandos > 0 else 0
	porcentaje_nmap = (contador_nmap / total_comandos * 100) if total_comandos > 0 else 0


	respuesta = f"Estadísticas de uso de comandos:\n"
	respuesta += f"/info: usado {contador_info} veces y su porcentaje es: ({porcentaje_info:.2f}%)\n"
	respuesta += f"/host_info: usado {contador_host_info} veces y su porcentaje es: ({porcentaje_host_info:.2f}%)\n"
	respuesta += f"/net_info: usado {contador_net_info} veces y su porcentaje es: ({porcentaje_net_info:.2f}%)\n"
	respuesta += f"/ping: usado {contador_ping} veces y su porcentaje es: ({porcentaje_ping:.2f}%)\n"
	respuesta += f"/errorlog: usado {contador_errorlog} veces y su porcentaje es: ({porcentaje_errorlog:.2f}%)\n"
	respuesta += f"/servicio: usado {contador_estado_servicio} veces y su porcentaje es: ({porcentaje_estado_servicio:.2f}%)\n"
	respuesta += f"/start_servicio: usado {contador_arrancar_servicio} veces y su porcentaje es: ({porcentaje_arrancar_servicio:.2f}%)\n"
	respuesta += f"/stop_servicio: usado {contador_apagar_servicio} veces y su porcentaje es: ({porcentaje_apagar_servicio:.2f}%)\n"
	respuesta += f"/puertos: usado {contador_puertos} veces y su porcentaje es: ({porcentaje_puertos:.2f}%)\n"
	respuesta += f"/nmap: usado {contador_nmap} veces y su porcentaje es: ({porcentaje_nmap:.2f}%)\n"


	contador_info = 0
	contador_host_info = 0
	contador_net_info = 0
	contador_ping = 0
	contador_errorlog = 0
	contador_estado_servicio = 0
	contador_arrancar_servicio = 0
	contador_apagar_servicio = 0
	contador_puertos = 0
	contador_nmap = 0


	await update.message.reply_text(respuesta)




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message when the command /start is issued."""

    user = update.effective_user

    await update.message.reply_html(

        rf"Hi {user.mention_html()}!",

        reply_markup=ForceReply(selective=True),

    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message when the command /help is issued."""

    await update.message.reply_text("Help!")



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Echo the user message."""

    await update.message.reply_text(update.message.text)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	bot_info = "Este es el bot de adrian"
	await update.message.reply_text(bot_info)

	global contador_info
	contador_info += 1

async def host_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	os_info = sys.platform

	respuesta_host_info = "Tu sistema operativo es: "+os_info
	await update.message.reply_text(respuesta_host_info)

	global contador_host_info
	contador_host_info += 1

async def net_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	lista_interfaces = netifaces.interfaces()
	for interfaz in lista_interfaces:
		addrs = netifaces.ifaddresses(interfaz)
		if netifaces.AF_INET in addrs:
			for addr_info in addrs[netifaces.AF_INET]:
				respuesta_net_info = "La direccion IP de "+interfaz+" es "+addr_info['addr']
				await update.message.reply_text(respuesta_net_info)

	global contador_net_info
	contador_net_info += 1

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	try:
		ip = context.args[0]

		ping = subprocess.getoutput(f'ping -c 4 {ip}')
		if '0% packet loss' in ping:
			await update.message.reply_text(f'Respuesta del ping a {ip}:\n\n{ping}')
		else:
			await update.message.reply_text(f'No se ha podido alcanzar la IP {ip}')
	except Exception as e:
		await update.message.reply_text(f'Error: {str(e)}')

	global contador_ping
	contador_ping += 1

async def error_log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	num_errores = context.args[0]

	with open('/var/log/syslog', 'r') as syslog:
		lineas = syslog.readlines()

	errores = [linea for linea in lineas if re.search(r'error', linea, re.IGNORECASE)]

	ultimos_errores = errores[-int(num_errores):]

	await update.message.reply_text('\n'.join(ultimos_errores))

	global contador_errorlog
	contador_errorlog += 1

async def service_running(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	servicio = context.args[0]

	existe = subprocess.getoutput(f'systemctl list-units --all --type service')

	if f'{servicio}.service' in existe:

		activo = subprocess.getoutput(f'systemctl is-active {servicio}')

		if activo == 'active':
			await update.message.reply_text(f'El servicio {servicio} esta activo')
		else:
			await update.message.reply_text(f'El servicio {servicio} no esta activo')

	else:

		await update.message.reply_text(f'El servicio {servicio} no existe')

	global contador_estado_servicio
	contador_estado_servicio += 1

async def service_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	servicio = context.args[0]

	existe = subprocess.getoutput(f'systemctl list-units --all --type service')

	if f'{servicio}.service' in existe:

		activo = subprocess.getoutput(f'systemctl is-active {servicio}')

		if activo == 'active':
			await update.message.reply_text(f'El servicio {servicio} ya esta iniciado')
		else:
			subprocess.getoutput(f'systemctl-iniciar {servicio}')
			await update.message.reply_text(f'Iniciando el servicio {servicio}')

	global contador_arrancar_servicio
	contador_arrancar_servicio += 1

async def service_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        servicio = context.args[0]

        existe = subprocess.getoutput(f'systemctl list-units --all --type service')

        if f'{servicio}.service' in existe:

                activo = subprocess.getoutput(f'systemctl is-active {servicio}')

                if activo == 'inactive':
                        await update.message.reply_text(f'El servicio {servicio} ya esta parado')
                else:
                        subprocess.getoutput(f'systemctl-parar {servicio}')
                        await update.message.reply_text(f'Parando el servicio {servicio}')

        global contador_apagar_servicio
        contador_apagar_servicio += 1

async def ports_in_use(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	puertos_info = []
	for conn in psutil.net_connections(kind='inet'):
		if conn.status == psutil.CONN_ESTABLISHED:
                	try:
                        	proceso = psutil.Process(conn.pid)
                        	programa = proceso.name()
                	except psutil.NoSuchProcess:
                        	programa = "Desconocido"
                	puertos_info.append(f"Puerto: {conn.laddr.port}, Programa: {programa}")

	if not puertos_info:
		await update.message.reply_text('No se encontraron puertos en este momento')
	else:
		await update.message.reply_text(f'Puertos en uso en este momento:\n'+'\n'.join(puertos_info))

	global contador_puertos
	contador_puertos += 1

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

	ip = context.args[0]

	nm = nmap.PortScanner()

	nm.scan(ip, arguments='-sP')

	respuesta = "Direcciones IP accesibles en la red:\n"
	for host in nm.all_hosts():
		respuesta += f"IP: {host}, Nombre: {nm[host].hostname()}\n"

	await update.message.reply_text(respuesta)

	global contador_nmap
	contador_nmap += 1


def main() -> None:

    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token("6515685212:AAHmTLS-LPKjd26FUbssVznqw5eJDjU31XE").build()


    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CommandHandler("estadisticas", statistics))

    application.add_handler(CommandHandler("info", info))

    application.add_handler(CommandHandler("host_info", host_info))

    application.add_handler(CommandHandler("net_info", net_info))

    application.add_handler(CommandHandler("ping", ping))

    application.add_handler(CommandHandler("servicio", service_running))

    application.add_handler(CommandHandler("start_servicio", service_start))

    application.add_handler(CommandHandler("stop_servicio", service_stop))

    application.add_handler(CommandHandler("puertos", ports_in_use))

    application.add_handler(CommandHandler("nmap", scan))

    application.add_handler(CommandHandler("errorlog", error_log))
    # on non command i.e message - echo the message on Telegram

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":

    main()
