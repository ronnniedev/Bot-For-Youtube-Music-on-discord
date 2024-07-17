from apikeys import *
import requests
import json

async def broma(ctx):
    
    url = "https://jokes-always.p.rapidapi.com/common"

    headers = {
	    "x-rapidapi-key": tokenBromas,
	    "x-rapidapi-host": "jokes-always.p.rapidapi.com"
    }

    response= requests.get(url, headers=headers)
    texto = json.loads(response.text)['data']
    # await ctx.send(texto)
     # formateamos el texto para que nos suelte un chiste
    
    url = "https://google-translator9.p.rapidapi.com/v2"

    payload = {
	    "q": texto,
	    "source": "en",
	    "target": "es",
	    "format": "text"
    }
    headers = {
	    "x-rapidapi-key": tokenBromas,
	    "x-rapidapi-host": "google-translator9.p.rapidapi.com",
	    "Content-Type": "application/json"
    }

    respuesta = requests.post(url, json=payload, headers=headers)
    #Convertimos la respuesta de jason en un dato de tipo diccionario 
    respuesta = respuesta.json() 
    """le indicamos donde esta el texto a escribir, le decimos que esta en data, seccion translations, elemento 0 y translated text"""
    texto = respuesta['data']['translations'][0]['translatedText'] 
    
    await ctx.send(texto)