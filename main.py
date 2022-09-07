import requests
import asyncio


async def get_url_image():
    request = 'https://api.thecatapi.com/v1/images/search'
    response = loop.run_in_executor(None, requests.get, request)
    await_response = await response
    image_url = await_response.json()[0]['url']
    return image_url


async def get_image(url):
    url_image = url
    response_image = loop.run_in_executor(None, requests.get, url_image)
    await_image = await response_image
    image_content = await_image.content
    print(f'Изображение получено, но не записано.')
    return image_content


async def cat_image():
    image = await get_url_image()
    image_name_and_extension = image.split('/')[-1]
    image_content = await get_image(image)
    await save_image(image_name_and_extension, image_content)


async def save_image(image_name_and_extension, image_content):
    with open(f'Cats/{image_name_and_extension}', 'wb+') as writer:
        writer.write(image_content)
        print(f'Изображение {image_name_and_extension} записано!')


number_needed_images = 20
loop = asyncio.get_event_loop()
tasks = [loop.create_task(cat_image()) for i in range(number_needed_images)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
