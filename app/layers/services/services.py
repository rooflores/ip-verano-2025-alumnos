# capa de servicio/lógica de negocio
import requests
import random 
from ...config import config
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user


# función que devuelve un listado de cards. Cada card representa una imagen de la API de HP.
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    # 2) convertir cada img. en una card.
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    # ATENCIÓN: contemplar que los nombres alternativos, para cada personaje, deben elegirse al azar. Si no existen nombres alternativos, debe mostrar un mensaje adecuado.
def getAllImages():
    json_collection = transport.getAllImages()
    imagenes = []
    
    for object in json_collection:
        card=translator.fromRequestIntoCard(object)
        if len(card.alternate_names)== 0:
            card.alternate_names="No tiene nombres alternativos"
        else:
            card.alternate_names=random.choice(card.alternate_names)
        imagenes.append(card)

    return imagenes        

# función que filtra según el nombre del personaje.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        if card.name==name:
            filtered_cards.append(card)
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.

    return filtered_cards

# función que filtra las cards según su casa.
def filterByHouse(house_name):
    filtered_cards = []

    for card in getAllImages():
        if card.house==house_name:
            filtered_cards.append(card)
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID