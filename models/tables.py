# -*- coding: utf-8 -*-

from datetime import datetime

db.define_table('posts',
                Field('senderID', 'reference auth_user'),
                Field('recieverID', 'reference auth_user'),
                Field('body', requires = IS_LENGTH(minsize = 1, maxsize = 300)),
                Field('likes', 'integer', default = 0),
                Field('approved', 'boolean', default = False),
                Field('flagged', 'boolean', default = False),
                Field('timePosted', 'datetime', default = datetime.utcnow()))

db.define_table('relationships',
                Field('userID', 'reference auth_user'),
                Field('friends', 'list:reference auth_user'),
                Field('favorites', 'list:reference auth_user'),
                Field('blocked', 'list:reference auth_user'),
                Field('pending', 'list:reference auth_user'))
