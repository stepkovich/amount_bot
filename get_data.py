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
            # # return await inf_art.json()
            #
            try:
                products = await inf_art.json()
                art = str(products[0]['art'])
                name = str(products[0]['name'])
                brand = str(products[0]['TM'])
                price = str(round(products[0]['price'] / 1.2, 2))


                async with session.get(
                        f'https://lk.iek.ru/api/products?format=jsonp&art={article}&entity=Certificates') as sert:
                    inf_serts = await sert.json()
                    s = inf_serts[0]["Certificates"]
                    info_sert = []
                    for doc in s:
                        name_sert = doc.get('name').strip()
                        url_sert = doc['file_ref']['uri'].strip()
                        info_sert.append(url_sert)
                    column_sert = '\n'.join(info_sert)
                    # return str(column_sert)

                async with session.get(f'https://lk.iek.ru/api/residues/json/?sku={article}') as inf_amount:
                    amounts = await inf_amount.json()
                    stores = amounts['stores']
                    print(stores)
                    stor = []
                    for store in stores.items():
                        id = store[0]
                        name_stor = store[1]['name']
                        items_store = amounts.get('shopItems')[0].get("residues").get(id)
                        if items_store == None:
                            items_store = 0
                        stor.append(f'{name_stor} : {items_store}')
                    column_stor = '\n'.join(stor)
                # print (items_store)
                return (
                    f'Артикул:  {art}\n\nНазвание:   {name}\n\nБренд:   {brand}\n\nЦена:   {price} базовая без НДС\n\nНаличие: \n{str(column_stor)}'
                    f'\n\nСсылки на сертификаты: {str(column_sert)}')

            except Exception as e:

                return (f"Что-то пошло не так :)\n"
                        f"Убедитесь что артикул верный\n\n"
                        f"Так же возможны работы на сервере\n\n"
                        f"{e}")


