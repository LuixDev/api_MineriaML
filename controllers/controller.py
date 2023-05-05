from flask import jsonify, request

from models.models import *

mod_admin= Models()

class controller():

    def  login(self):
        query=mod_admin.login()
        return query
    
    def  getAll(self):
        query=mod_admin.getAll()
        return query
    
    def  getAlcohol(self):
        query=mod_admin.getAlcohol()
        return query
        
    def  predecir(self):
        query=mod_admin.predecir()
        return query
    
    def  getQuality(self):
        query=mod_admin.getQuality()
        return query
        
        
        
        
    
    