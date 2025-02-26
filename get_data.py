import requests
from config import LOGIN, PASWORD
from pprint import pprint


def get_info(artt):
    # r = requests.get(f'https://lk.iek.ru/api/products?format=jsonp&art=MRD10-16', auth=(LOGIN, PASWORD))
    # print(r)

    try:
        # get info product
        r = requests.get(f'https://lk.iek.ru/api/products?format=jsonp&art={artt}', auth=(LOGIN, PASWORD))
        product = r.json()[0]

        art = product['art']
        name = product['name']
        brand = product['TM']
        price = round(product['price'] / 1.2, 2)

        # get amount product
        r = requests.get(f'https://lk.iek.ru/api/residues/json/?sku={artt}', auth=(LOGIN, PASWORD))
        amount = r.json()

        stores = amount['stores']
        stor = []
        for store in stores.items():
            id = store[0]
            name_stor = store[1]['name']
            items_store = amount.get('shopItems')[-1].get('residues')[id]
            stor.append(f'{name_stor} : {items_store}')
        column_stor = '\n'.join(stor)

        return (
            f'Артикул:  {art}\n\nНазвание:   {name}\n\nБренд:   {brand}\n\nЦена:   {price} базовая без НДС\n\nНаличие: \n{column_stor}')

    except:

        return ("Что-то не так!\nПроверьте артикул...")


def get_sertificats(artt):
    try:
        # get info product
        r = requests.get(f'https://lk.iek.ru/api/products?format=jsonp&art={artt}&entity=Certificates',
                         auth=(LOGIN, PASWORD))
        serts = r.json()[0]["Certificates"]

        info_sert = []
        for sert in serts:
            name_sert = sert.get('name').strip()
            url_sert = sert['file_ref']['uri'].strip()
            info_sert.append(f'\n{"―" * 16}\n{name_sert}:\n{url_sert}\n{"―" * 16}')
        column_sert = '\n'.join(info_sert)

        # return(f'\n{"-"*30}\n{name_sert}\n{url_sert}\n{"-"*30}')
        return (column_sert)


    except:
        return ("Что-то не так!\nПроверьте артикул...")


def get_analog(artt):
    try:
        r = requests.get(f'https://lk.iek.ru/api/products?format=jsonp&art={artt}&entity=Analog', auth=(LOGIN, PASWORD))
        analogs = r.json()[0]["Analog"]

        info_analog = []
        for analog in analogs:
            if not analog.get('analog'):
                art_analog = "Нет Аналога"
            else:
                art_analog = analog.get('analog').strip()

            if not analog['desc']:
                descr = "Нет описания отличий"

            else:
                descr = analog['desc']

            info_analog.append(f'\n{"―" * 16}\nАртикул:     {art_analog}:\nОтличается:     {descr}\n{"―" * 16}')

        column_analog = '\n'.join(info_analog)

        return (column_analog)

    except:
        return ("Нет информации")
