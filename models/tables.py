# -*- coding: utf-8 -*-

from datetime import datetime

db.define_table('posts',
                Field('senderID', 'reference auth_user'),
                Field('recieverID', 'reference auth_user'),
                Field('body'),
                Field('likes', 'integer'),
                Field('approved', 'boolean'),
                Field('flagged', 'boolean'),
                Field('timePosted', 'datetime'))

db.define_table('relationships',
                Field('friends', 'list:reference auth_user'),
                Field('favorites', 'list:reference auth_user'),
                Field('blocked', 'list:reference auth_user'),
                Field('pending', 'list:reference auth_user'))
