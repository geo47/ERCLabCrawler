import os.path

import yaml
from config import Config as cfg

yaml.warnings({'YAMLLoadWarning': False})

class YelpConfig:

    def __init__(self):

        for filename in os.listdir(cfg.template_path):
            abs_file_path = os.path.abspath("template/yelp-site.yaml")
            with open(abs_file_path, 'r') as yaml_file:
                self.yelp_site = yaml.load(yaml_file)

    def get_template(self):
        return self.yelp_site["template"]

    def get_menu(self):
        return self.yelp_site["menu"]