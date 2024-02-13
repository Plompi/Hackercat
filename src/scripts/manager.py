import os
import nextcord as discord
from PIL import Image
from io import BytesIO

class ImageManager:
    def __init__(self, bot, path, channelid):
        self.bot = bot
        self.PATH = path
        self.DATABASE_CHANNEL = channelid
        self.update_SORTEDDIR()

    def get_PATH(self):
        return self.PATH

    def get_SORTEDDIR(self):
        return self.SORTEDDIR

    def get_data_size(self):
        return self.data_size

    def update_SORTEDDIR(self):
        self.SORTEDDIR = sorted(os.scandir(self.PATH), key = lambda x: x.stat().st_mtime)
        self.data_size = len(self.SORTEDDIR) - 1

    def get_Image(self, image):
        name = self.SORTEDDIR[image].name
        embed = discord.Embed(title = f'Image {image}/{self.data_size}')
        embed.set_image(url = f'attachment://{name}')
        return embed, discord.File(f'{self.PATH}/{name}')

    def del_Image(self, image):
        os.remove(self.get_SORTEDDIR()[image])
        self.update_SORTEDDIR()
        return self.data_size

    async def add_Image(self, message):
        for attachment in message.attachments:
            if attachment.filename.endswith(('.png', '.jpg', '.jpeg')):
                if attachment.filename in os.listdir(self.PATH):
                    continue
            
                #print(attachment.url) //If cdn-url does not expire -> switch from local file storage to cdn
                image = Image.open(BytesIO(await attachment.read())).convert('RGB')
                image.save(f'{self.PATH}/{attachment.filename}', format = 'JPEG', optimize = True, quality = 20)
        await message.delete()

    async def read_historical_messages(self):
        channel = self.bot.get_channel(self.DATABASE_CHANNEL)
        async for message in channel.history(limit = None, oldest_first = True):
            await self.add_Image(message)
        self.update_SORTEDDIR()