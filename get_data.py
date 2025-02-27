import asyncio
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

LOG = os.getenv("LOGIN")
PASW = os.getenv("PASWORD")


async def get_info_async(article):
    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(LOG, PASW)) as session:
        async with session.get(f'https://lk.iek.ru/api/products?format=jsonp&art={article}') as inf_art:
            try:
                products = await inf_art.json()
                art = products[0]['art']
                name = products[0]['name']
                brand = products[0]['TM']
                price = round(products[0]['price'] / 1.2, 2)

                async with session.get(f'https://lk.iek.ru/api/residues/json/?sku={article}') as inf_amount:
                    amounts = await inf_amount.json()
                    stores = amounts['stores']
                    stor = []
                    for store in stores.items():
                        id = store[0]
                        name_stor = store[1]['name']
                        items_store = amounts.get('shopItems')[-1].get('residues')[id]
                        stor.append(f'{name_stor} : {items_store}')
                    column_stor = '\n'.join(stor)

                async with session.get(
                        f'https://lk.iek.ru/api/products?format=jsonp&art={article}&entity=Certificates') as sert:
                    inf_serts = await sert.json()
                    s = inf_serts[0]["Certificates"]
                    info_sert = []
                    for doc in s:
                        name_sert = doc.get('name').strip()
                        url_sert = doc['file_ref']['uri'].strip()
                        # info_sert.append(f'\n{"―" * 16}\n{name_sert}:\n{url_sert}\n{"―" * 16}')
                        info_sert.append(url_sert)
                    column_sert = '\n'.join(info_sert)

                return (
                    f'Артикул:  {art}\n\nНазвание:   {name}\n\nБренд:   {brand}\n\nЦена:   {price} базовая без НДС\n\nНаличие: \n{column_stor}'
                    f'\n\nСсылки на сертификаты: {column_sert}')
            except:

                return (f"Что-то пошло не так :)\n"
                        f"Убедитесь что артикул верный\n\n"
                        f"Так же возможны работы на сервере")

# async def answer(command):
#     # for s in info_sert:
#         return info_sert[-1]


# asyncio.run(get_info_async("CKK11-100-060-1-K01"))
# asyncio.run(answer("CKK11-100-060-1-K01"))

# async def get_info(session, article):
#     try:
#         # get info product
#         async with session.get(f'https://lk.iek.ru/api/products?format=jsonp&art={article}') as response:
#             product = await response.json()
#             art = product[0]['art']
#             name = product[0]['name']
#             brand = product[0]['TM']
#             price = round(product[0]['price'] / 1.2, 2)

# # get amount product
# r = requests.get(f'https://lk.iek.ru/api/residues/json/?sku={artic}', auth=(LOG, PASW))
# amount = r.json()
#
# stores = amount['stores']
# stor = []
# for store in stores.items():
#     id = store[0]
#     name_stor = store[1]['name']
#     items_store = amount.get('shopItems')[-1].get('residues')[id]
#     stor.append(f'{name_stor} : {items_store}')
# column_stor = '\n'.join(stor)
#
#     return (f'Артикул:  {art}\n\nНазвание:   {name}\n\nБренд:   {brand}\n\nЦена:   {price} базовая без НДС\n\n')
#     # f'Наличие: \n{column_stor}')
#
# except:
#
#     return ("Что-то не так!\nПроверьте артикул...")

# asyncio.run(get_info_async("CKK11-100-060-1-K01"))

# def get_sertificats(artic):
#     try:
#         # get info product
#         r = requests.get(f'https://lk.iek.ru/api/products?format=jsonp&art={artic}&entity=Certificates',
#                          auth=(LOG, PASW))
#         serts = r.json()[0]["Certificates"]
#
#         info_sert = []
#         for sert in serts:
#             name_sert = sert.get('name').strip()
#             url_sert = sert['file_ref']['uri'].strip()
#             info_sert.append(f'\n{"―" * 16}\n{name_sert}:\n{url_sert}\n{"―" * 16}')
#         column_sert = '\n'.join(info_sert)
#
#         # return(f'\n{"-"*30}\n{name_sert}\n{url_sert}\n{"-"*30}')
#         return column_sert
#
#
#     except:
#         return "Что-то не так!\nПроверьте артикул..."
# #
# #
# # def get_analog(artic):
# #     try:
# #         r = requests.get(f'https://lk.iek.ru/api/products?format=jsonp&art={artic}&entity=Analog', auth=(LOG, PASW))
# #         analogs = r.json()[0]["Analog"]
# #
# #         info_analog = []
# #         for analog in analogs:
# #             if not analog.get('analog'):
# #                 art_analog = "Нет Аналога"
# #             else:
# #                 art_analog = analog.get('analog').strip()
# #
# #             if not analog['desc']:
# #                 descr = "Нет описания отличий"
# #
# #             else:
# #                 descr = analog['desc']
# #
# #             info_analog.append(f'\n{"―" * 16}\nАртикул:     {art_analog}:\nОтличается:     {descr}\n{"―" * 16}')
# #
# #         column_analog = '\n'.join(info_analog)
# #
# #         return column_analog
# #
# #     except:
# #         return "Нет информации"
