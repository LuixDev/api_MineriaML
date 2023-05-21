from flask import Flask, jsonify, request, Blueprint
from flask_cors import  cross_origin
from controllers.controller import *


conexion= controller()



usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/login', methods=['POST'])
@cross_origin()  
def login():
   return conexion.login()


@usuarios.route('/consultar', methods=['GET'])
@cross_origin()
def getAll():
   return conexion.getAll()


@usuarios.route('/alcohol', methods=['GET'])
@cross_origin()
def getAlcohol():
   return conexion.getAlcohol()

@usuarios.route('/quality', methods=['GET'])
@cross_origin()
def getQuality():
   return conexion.getQuality()

@usuarios.route('/predecir', methods=['POST'])
@cross_origin()
def predecir():
   return conexion.predecir()

@usuarios.route('/enviar', methods=['POST'])
@cross_origin()
def enviar():
   return conexion.enviar()


@usuarios.route('/getn', methods=['GET'])
@cross_origin()
def getn():
   return conexion.getn()

@usuarios.route('/eliminar', methods=['POST'])
@cross_origin()
def eliminar_notificacion():
   return conexion.eliminar_notificacion()


@usuarios.route('/survived', methods=['GET'])
@cross_origin()
def getSurvived():
   return conexion.getSurvived()

@usuarios.route('/psa', methods=['GET'])
@cross_origin()
def getPsa():
   return conexion.getPsa()

@usuarios.route('/age', methods=['GET'])
@cross_origin()
def getAge():
   return conexion.getAge()