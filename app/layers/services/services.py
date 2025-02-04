# capa de servicio/lógica de negocio

import random     #ealiza una seleccion de forma aleatoria
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de HP.
def getAllImages():
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    # 2) convertir cada img. en una card.
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    # ATENCIÓN: contemplar que los nombres alternativos, para cada personaje, deben elegirse al azar. Si no existen nombres alternativos, debe mostrar un mensaje adecuado.
    
    raw_images = transport.getAllImages() 
    card_list = []
    for img in raw_images:
            card = {
                "id": img.get("id"),
                "name": img.get("name"), 
                "alternate_names": random.choice(img.get("alternate_names", []) or ["Nombre desconocido"]),
                "gender": img.get("gender"),
                "house": img.get("house", "Desconocida"),
                "image": img.get("image"),
                "actor": img.get("actor"),
            }
            card_list.append(card)

    return card_list 

    pass

# función que filtra según el nombre del personaje.
def filterByCharacter(name):
    all_images = getAllImages()  # Obtiene todas las imágenes de transport.py
    filtered_cards = []

    # Filtramos las imágenes que contienen el nombre ingresado, ignorando mayúsculas/minúsculas
    for img in all_images:
        if name.lower() in img['name'].lower():  # Compara el nombre de la imagen con el nombre ingresado
            filtered_cards.append(img)

    return filtered_cards

# función que filtra las cards según su casa.
def filterByHouse(house_name):
    all_images = getAllImages() #obtiene todas las imagenes de transport.py
    filtered_cards = []

    for card in all_images:
        if card.get('house') == house_name:  # Si la casa de la imagen coincide con la casa proporcionada
            filtered_cards.append(card)  # Agrega la imagen a la lista de filtradas

    return filtered_cards  # Devuelve la lista de imágenes filtradas


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
