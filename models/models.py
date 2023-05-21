from config import *
from flask import jsonify, request
import jwt
import pickle
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import json 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import numpy as np









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
   


   def getn(self):
    cur = connection.cursor()
    cur.execute('SELECT * FROM contacto')
    rv = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for result in rv:
       content = {'id': result[0], 'name': result[1], 'email': result[2], 'message': result[3]}
       payload.append(content)
    return jsonify(payload)


   def eliminar_notificacion(self):
     
     data = request.get_json()
     id = data['id']
     responder = data['responder']
     email = data['email']
     cur = connection.cursor()
     cur.execute('DELETE FROM  contacto WHERE id = %s', (id,))
     connection.commit()
     cur.execute('SELECT * FROM contacto')
     cur.fetchall()
     smtp_host = 'smtp-mail.outlook.com'
     smtp_port = 587
     username = 'gwermk@hotmail.com'
     password = 'Ht56848*'

     from_email = 'gwermk@hotmail.com'
     to_email =   email
     subject = 'MiningML'
     body = responder

     # Crea el objeto MIMEText con el cuerpo del mensaje
     message = MIMEMultipart()
     message['From'] = from_email
     message['To'] = to_email
     message['Subject'] = subject
     message.attach(MIMEText(body, 'plain'))

    # Establece la conexión SMTP y envía el correo electrónico
     with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(message)

     return jsonify("Mensaje enviado")





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
   

   def getSurvived(self):
    cur = connection.cursor()
    cur.execute('SELECT CAST(survived AS INTEGER) FROM titanic')  # Conversión explícita a enteros
    results = cur.fetchall()
    cur.close()

    survived_data = [result[0] for result in results]  # Almacenar los datos en un arreglo

    count_yes = survived_data.count(1)  # Contar el número de ocurrencias del valor 1 (sí)
    print("hola probando",count_yes)
    return jsonify(count_yes)


   def getPsa(self):
    print("total pasajero 892 porque es el total de dato que estamos utilizando")
    num="892"
    return jsonify(num)

   def getAge(self):
    cur = connection.cursor()
    cur.execute('SELECT age FROM titanic')
    results = cur.fetchall()
    numeros = [float(tupla[0]) for tupla in results if tupla[0] is not None]
    valor_maximo = max(numeros)
    numero_entero = int(valor_maximo)
    print(numero_entero)
    cur.close()

    return jsonify(numero_entero)


 

   def predecir(self):
    archivo = request.files['file']
    text1 = request.form['text1']
    nombre_archivo = secure_filename(archivo.filename)
 
    archivo.save(nombre_archivo)
    df = pd.read_csv(nombre_archivo, delimiter=';', encoding='utf-8')

    # Verificar si la columna 'alcohol' está presente en el DataFrame

    # Obtener las características (X) y la variable objetivo (y) del DataFrame
    X = df.drop(text1, axis=1)
    y = df[text1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

    # Instanciar el modelo de Bosque Aleatorio
    rf = RandomForestRegressor(n_estimators=100, random_state=42)

    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    score = r2_score(y_test, y_pred)

    # Crear el diccionario de resultados
    resultados = {
        "----SCORE": score,
        "----MSE": mse,
        "----Predicciones": y_pred.tolist()
    }

    return jsonify(resultados)


   

   def enviar(self):
        data = request.get_json()
        name = data['name']
        message = data['message']
        email = data['email']

        # Verificar el nombre de usuario y la contraseña en la base de datos
        cursor = connection.cursor()
        cursor.execute("INSERT INTO contacto  (name,message,email) VALUES (%s, %s,%s)", (name,message,email))
        connection.commit()
        smtp_host = 'smtp-mail.outlook.com'
        smtp_port = 587
        username = 'gwermk@hotmail.com'
        password = 'Ht56848*'

        # Configura los detalles del correo electrónico
        from_email = 'gwermk@hotmail.com'
        to_email =   email
        subject = 'Gracias por contactarnos'
        body = 'Hemos recibido tu mensajes'

        # Crea el objeto MIMEText con el cuerpo del mensaje
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Establece la conexión SMTP y envía el correo electrónico
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(message)

        print('Correo electrónico enviado')
        response = {
        'success': True,
        'message': 'Dato creado exitosamente'
    }

               
            
        
        return jsonify(response)
   
   




   


