import json
import os

class Config:
    def __init__(self):
        self.path = os.path.dirname(os.path.dirname(__file__))
        self.config_json_path = os.path.join(self.path, os.path.join('config','config.json'))
        self.DATABASE_PATH = os.path.join(self.path, 'database')
        self.IMAGE_PATH = os.path.join(self.path, 'img')
        self.load_config()

    def all_extensions(self):
        return [f'src.extensions.{ext[:-3]}' for ext in os.listdir(os.path.join(self.path, 'extensions')) if ext.endswith('.py')]

    def save(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            with open(self.config_json_path, 'w') as config_file:
                json.dump(self.data, config_file, indent=4)
            self.load_config()
            return result
        return wrapper

    
    def load_config(self):
        try:
            with open(self.config_json_path, 'r') as config_file:
                self.data = json.load(config_file)

        except FileNotFoundError:
            config_path = os.path.join(self.path, 'config')
            if not os.path.exists(config_path):
                os.makedirs(config_path)
            self.data = {   'TOKEN': str(input('Enter the Token of your Discord Bot:')),
                            'DATABASE_DISCORD_CHANNEL_ID': None,
                            'ADMINS': {},
                            'OWNER':{},
                            'EXTENSIONS': [all_extensions()],
                            'MENUS': {}}

            with open(self.config_json_path, 'w') as config_file:
                json.dump(self.data, config_file, indent=4)

        finally:
            self.TOKEN = self.data['TOKEN']
            self.DATABASE_DISCORD_CHANNEL_ID = self.data['DATABASE_DISCORD_CHANNEL_ID']
            self.ADMINS = self.data['ADMINS']
            self.OWNER = self.data['OWNER']
            self.MENU = self.data['MENUS']
            self.EXTENSIONS = self.data['EXTENSIONS']
    
    @save
    def add_admin(self, user):
        self.data['ADMINS'][user.name] = user.id
        
    @save
    def del_admin(self, user):
        del self.data['ADMINS'][user.name]

    @save
    def add_owner(self, user):
        self.data['OWNER'][user.name] = user.id
        
    @save
    def del_owner(self, user):
        del self.data['OWNER'][user.name]
        
    @save
    def set_channel(self, channel):
        self.data['DATABASE_DISCORD_CHANNEL_ID'] = channel.id

    @save
    def set_menu(self, name, *args):
        self.data['MENUS'][name] = args

    @save
    def toggle_extension(self, name):
        if name in self.data['EXTENSIONS']:
            self.data['EXTENSIONS'].remove(name)
        else:
            self.data['EXTENSIONS'].append(name)