#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

''' eth utilities module '''

import json
import yaml

def json_to_yamler(json_dump):
    ''' converts from json to yaml output '''
    json_dumped = json.dumps(json_dump)
    yamled_dict = yaml.safe_load(json_dumped)
    return yamled_dict

