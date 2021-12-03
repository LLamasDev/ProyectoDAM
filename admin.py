#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import subprocess
import os 
from data import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
#logger.setLevel(logging.DEBUG) Modo DEBUG
logger.setLevel(logging.INFO)

proceso_seleccionado = '' # Variable global con la que gestionaremos los procesos
proceso_seleccionado_completo = '' # Variable global con el nombre completo del proceso

def main_menu_keyboard(): # Menu inicial
    keyboard = [[InlineKeyboardButton('Resultados de Fútbol', callback_data='resultadosfutbol')], [InlineKeyboardButton('Supercell', callback_data='supercell')], [InlineKeyboardButton('Clash Royale', callback_data='clashroyale')], [InlineKeyboardButton('Clash of Clans', callback_data='clashofclans')]]

    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard_all(): # Menu del proceso
    keyboard = [[InlineKeyboardButton('Menú principal', callback_data='menu_principal')], [InlineKeyboardButton('Estado', callback_data='menu_estado')], [InlineKeyboardButton('Arrancar', callback_data='menu_arrancar'), InlineKeyboardButton('Parar', callback_data='menu_parada')], [InlineKeyboardButton('Reiniciar', callback_data='menu_reinicio')]]

    return InlineKeyboardMarkup(keyboard)

def main():
    updater = Updater(TOKENADMIN, use_context=True)
    ud = updater.dispatcher
    ud.add_handler(CommandHandler('start', start))
    ud.add_handler(CommandHandler('arrancartodo', arrancar_todo))
    ud.add_handler(CommandHandler('parrartodo', parrar_todo))
    ud.add_handler(CommandHandler('reiniciartodo', reiniciar_todo))
    ud.add_handler(CommandHandler('actualizarfutbol', resultados_futbol_actualizar))
    ud.add_handler(CallbackQueryHandler(menu_bot_cambio, pattern='resultadosfutbol'))
    ud.add_handler(CallbackQueryHandler(menu_bot_cambio, pattern='supercell'))
    ud.add_handler(CallbackQueryHandler(menu_bot_cambio, pattern='clashroyale'))
    ud.add_handler(CallbackQueryHandler(menu_bot_cambio, pattern='clashofclans'))
    ud.add_handler(CallbackQueryHandler(menu_bot_principal, pattern='menu_principal'))
    ud.add_handler(CallbackQueryHandler(menu_bot_estado, pattern='menu_estado'))
    ud.add_handler(CallbackQueryHandler(menu_bot_arranque, pattern='menu_arrancar'))
    ud.add_handler(CallbackQueryHandler(menu_bot_parada, pattern='menu_parada'))
    ud.add_handler(CallbackQueryHandler(menu_bot_reinicio, pattern='menu_reinicio'))
    updater.start_polling()
    updater.idle()

# Menus
def start(update, context):
    chatId = update.message.from_user.id

    if chatId == miID: # Si el ID no es el mio no hago nada
        update.message.reply_text('Todos los bots:', reply_markup=main_menu_keyboard())

def menu_bot_principal(update, context):
    query = update.callback_query

    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='Todos los bots:', reply_markup=main_menu_keyboard())

def menu_bot_cambio(update, context): # Cambio las variables globales
    query = update.callback_query
    query.answer # Saco lo pulsado en el boton
    global proceso_seleccionado, proceso_seleccionado_completo
    proceso_seleccionado = query.data # Cambio la variable global a lo pulsado en el boton que es el proceso que quiero tocar

    if proceso_seleccionado == 'supercell':
        proceso_seleccionado_completo = 'Supercell @SupercellAPIBot'
    elif proceso_seleccionado == 'clashroyale':
        proceso_seleccionado_completo = 'Clash Royale @ClashRoyaleAPIBot'
    elif proceso_seleccionado == 'clashofclans':
        proceso_seleccionado_completo = 'Clash of Clans @ClashOfClansAPIBot'
    elif proceso_seleccionado == 'resultadosfutbol':
        proceso_seleccionado_completo = 'Resultados de Fútbol @ResultadosFutb0lBot'
    
    menu_bot_estado(update, context)

# Ejecutar comandos en bash
def arrancar_todo(update, context):
    chatId = update.message.from_user.id

    if chatId == miID: # Si el ID no es el mio no hago nada
        proceso_seleccionado_arranquetodo = './start_all.sh '
        texto_salida = subprocess.check_output([proceso_seleccionado_arranquetodo], universal_newlines=True, shell=True) #texto_salida = subprocess.run(['ls', '-a'], capture_output=True, text=True)

        update.message.reply_text(text=texto_salida)

def parrar_todo(update, context):
    chatId = update.message.from_user.id

    if chatId == miID: # Si el ID no es el mio no hago nada
        proceso_seleccionado_paradatodo = './stop_all.sh '
        texto_salida = subprocess.check_output([proceso_seleccionado_paradatodo], universal_newlines=True, shell=True) #texto_salida = subprocess.run(['ls', '-a'], capture_output=True, text=True)

        update.message.reply_text(text=texto_salida)

def reiniciar_todo(update, context):
    chatId = update.message.from_user.id

    if chatId == miID: # Si el ID no es el mio no hago nada
        proceso_seleccionado_reiniciotodo = './reboot_all.sh '
        texto_salida = subprocess.check_output([proceso_seleccionado_reiniciotodo], universal_newlines=True, shell=True) #texto_salida = subprocess.run(['ls', '-a'], capture_output=True, text=True)

        update.message.reply_text(text=texto_salida)

def menu_bot_estado(update, context):
    query = update.callback_query
    global proceso_seleccionado, proceso_seleccionado_completo
    proceso_seleccionado_estado = './procesos.sh ' + proceso_seleccionado
    texto_salida = subprocess.check_output([proceso_seleccionado_estado], universal_newlines=True, shell=True) #texto_salida = subprocess.run(['ls', '-a'], capture_output=True, text=True)

    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=proceso_seleccionado_completo + ':\n' + texto_salida, reply_markup=main_menu_keyboard_all())

def menu_bot_arranque(update, context):
    query = update.callback_query
    global proceso_seleccionado, proceso_seleccionado_completo
    proceso_seleccionado_arranque = './start.sh ' + proceso_seleccionado
    texto_salida = subprocess.check_output([proceso_seleccionado_arranque], universal_newlines=True, shell=True)

    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=proceso_seleccionado_completo + ':\n' + texto_salida, reply_markup=main_menu_keyboard_all())

def menu_bot_parada(update, context):
    query = update.callback_query
    global proceso_seleccionado, proceso_seleccionado_completo
    proceso_seleccionado_parada = './stop.sh ' + proceso_seleccionado
    texto_salida = subprocess.check_output([proceso_seleccionado_parada], universal_newlines=True, shell=True)

    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=proceso_seleccionado_completo + ':\n' + texto_salida, reply_markup=main_menu_keyboard_all())

def menu_bot_reinicio(update, context):
    query = update.callback_query
    global proceso_seleccionado, proceso_seleccionado_completo
    proceso_seleccionado_reinicio = './reboot.sh ' + proceso_seleccionado
    texto_salida = subprocess.check_output([proceso_seleccionado_reinicio], universal_newlines=True, shell=True)

    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=proceso_seleccionado_completo + ':\n' + texto_salida, reply_markup=main_menu_keyboard_all())

def resultados_futbol_actualizar(update, context):
    query = update.callback_query
    os.system("python3.6 sacar_resultados.py") # Tiene que ser 3.6 ya que cloudscraper trabaja con esa version

    update.message.reply_text('Datos actualizados 😄')

if __name__ == '__main__':
    main()
