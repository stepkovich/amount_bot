import asyncio
import os
import traceback  # Добавлено для вывода полной ошибки
from dotenv import load_dotenv
import aiohttp

load_dotenv()

LOG = os.getenv("LOGIN")
PASW = os.getenv("PASWORD")


async def get_info_async(article):
    # Используем params для безопасной передачи артикула в URL
    params_art = {'format': 'jsonp', 'art': article}
    params_cert = {'format': 'jsonp', 'art': article, 'entity': 'Certificates'}
    params_residues = {'sku': article}

    auth = aiohttp.BasicAuth(LOG, PASW)

    async with aiohttp.ClientSession(auth=auth) as session:
        try:
            # 1. Получаем основную информацию
            async with session.get('https://lk.iek.ru/api/products', params=params_art) as inf_art:
                products = await inf_art.json()
                if not products:
                    return "Товар не найден. Проверьте артикул."

                product = products[0]
                art = str(product.get('art', 'Не указан'))
                name = str(product.get('name', 'Не указано'))
                brand = str(product.get('TM', 'Не указан'))
                price_raw = product.get('price', 0)
                price = str(round(price_raw / 1.2, 2)) if price_raw else "Нет данных"

            # 2. Получаем сертификаты
            column_sert = "Нет сертификатов"
            async with session.get('https://lk.iek.ru/api/products', params=params_cert) as sert:
                inf_serts = await sert.json()
                if inf_serts and inf_serts[0].get("Certificates"):
                    s = inf_serts[0]["Certificates"]
                    info_sert = []
                    for doc in s:
                        # Безопасное извлечение ссылки
                        file_ref = doc.get('file_ref')
                        if file_ref and file_ref.get('uri'):
                            url_sert = file_ref['uri'].strip()
                            info_sert.append(url_sert)

                    if info_sert:
                        column_sert = '\n'.join(info_sert)

            # 3. Получаем остатки
            column_stor = "Нет данных о наличии"
            async with session.get('https://lk.iek.ru/api/residues/json/', params=params_residues) as inf_amount:
                amounts = await inf_amount.json()
                stores = amounts.get('stores', {})

                # Безопасно достаем residues
                shop_items = amounts.get('shopItems')
                residues = {}
                if shop_items and len(shop_items) > 0:
                    residues = shop_items[0].get('residues', {})

                stor = []
                for store_id, store_data in stores.items():
                    name_stor = store_data.get('name', 'Магазин')
                    # Получаем остаток, если нет - 0
                    items_store = residues.get(store_id, 0)
                    stor.append(f'{name_stor} : {items_store}')

                if stor:
                    column_stor = '\n'.join(stor)

            return (
                f'Артикул: {art}\n\n'
                f'Название: {name}\n\n'
                f'Бренд: {brand}\n\n'
                f'Цена: {price} базовая без НДС\n\n'
                f'Наличие:\n{column_stor}\n\n'
                f'Ссылки на сертификаты:\n{column_sert}'
            )

        except Exception as e:
            # Если снова будет ошибка, бот пришлет ПОЛНЫЙ лог в чат!
            error_log = traceback.format_exc()
            return (f"Что-то пошло не так :)\n"
                    f"Убедитесь что артикул верный\n\n"
                    f"Полная ошибка для разработчика:\n{error_log}")