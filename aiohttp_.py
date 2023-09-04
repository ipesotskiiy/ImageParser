import asyncio
import aiohttp


class ImageDownloader:
    SEARCH_RANDOM_IMAGES_URL = 'https://api.thecatapi.com/v1/images/search'

    def __init__(self, loop, number_needed_images=2):
        self.number_needed_images = number_needed_images
        self.loop = loop

    def __call__(self, number_needed_images=2):
        tasks = [self.loop.create_task(self.get_and_save_cat_image()) for _ in range(
            number_needed_images if number_needed_images else self.number_needed_images)]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.loop.close()
        return self.get_and_save_cat_image()

    async def get_url_image(self, session):
        async with session.get(self.SEARCH_RANDOM_IMAGES_URL) as response:
            data = await response.json()
            return data[0]['url']

    async def get_image_content(self, url_image, session):
        async with session.get(url_image) as image_manager:
            response_image = await image_manager.read()
            return response_image

    async def get_and_save_cat_image(self):
        async with aiohttp.ClientSession() as session:
            url_image = await self.get_url_image(session)
            name_and_extension_image = url_image.split('/')[-1]
            content_image = await self.get_image_content(url_image, session)
            await self.loop.run_in_executor(None, self.save_image, name_and_extension_image, content_image)

    def save_image(self, name_and_extension_image, content_image):
        with open(f'Cats/{name_and_extension_image}', 'wb+') as writer:
            writer.write(content_image)
            print(f'Изображение {name_and_extension_image} записано!')


def main():
    loop = asyncio.get_event_loop()
    image_parser = ImageDownloader(loop, number_needed_images=5)
    image_parser(5)


if __name__ == "__main__":
    main()