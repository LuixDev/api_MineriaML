from config import *
from flask import jsonify, request
import jwt
import pickle
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import json 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split




class Models():
    
    

    
   def login(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Verificar el nombre de usuario y la contraseña en la base de datos
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM login WHERE usuario=%s AND contraseña=%s", (username, password))
        user = cursor.fetchone()

        if  user:
            token_payload = {
            'sub': user[0],
            'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(token_payload, 'secret', algorithm='HS256')


            response = {
            'success': True,
            'message': 'Login exitoso',
            'token': token
        }
        else:
            response = {
            'success': False,
            'message': 'Usuario o contraseña incorrectos'
        }
               
            
        
        return jsonify(response)
   


   def getAll(self):
        cur = connection.cursor()
        cur.execute('SELECT * FROM gestion')
        rv = cur.fetchall()
        cur.close()

        # Generar una lista vacía de objetos
        payload = []

        # Agregar cada objeto a la lista de objetos
        for result in rv:
            obj = {
                'fixed acidity': result[0],
                'volatile acidity': result[1],
                'citric acid': result[2],
                'residual sugar': result[3],
                'chlorides': result[4],
                'free sulfur dioxide': result[5],
                'total sulfur dioxide': result[6],
                'density': result[7],
                'pH': result[8],
                'sulphates': result[9],
                'alcohol': result[10],
                'quality': result[11]
            }
            payload.append(obj)

        # Devolver la lista de objetos como JSON
        return jsonify(payload)
   
   def getAlcohol(self):
    cur = connection.cursor()
    cur.execute('SELECT alcohol FROM gestion LIMIT 1')
    result = cur.fetchone()
    cur.close()

    # Devolver el dato como JSON
    return jsonify({'alcohol': result[0]})
   
   def getQuality(self):
    cur = connection.cursor()
    cur.execute('SELECT quality FROM gestion LIMIT 1')
    result = cur.fetchone()
    cur.close()

    # Devolver el dato como JSON
    return jsonify({'quality': result[0]})

 

   def predecir(self):
    # Obtenemos el tamaño de la casa del usuario
    data = request.get_json()
    mensaje = data['mensaje']
    
    df = pd.DataFrame({'columna_1': [1, 2, 3, 4, 5, 6, 7, 8], 'columna_mensaje': [3, 2, 1, 5, 6, 7, 8, mensaje]})
   
    # Realizamos la predicción con el modelo de Bosque Aleatorio
    X = df.drop(columns=['columna_mensaje'])
    y = df['columna_mensaje']

    # dividir los datos en conjunto de entrenamiento y conjunto de prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # instanciar el modelo de bosque aleatorio
    rf = RandomForestRegressor(n_estimators=100, random_state=42)

    # entrenar el modelo
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test) 
    score = r2_score(y_test, y_pred)
  
    return jsonify({'y_pred': list(y_pred), 'score': f"R2 score: {score:.3f}"})
   


