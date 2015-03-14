# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    return dict()

def profile():
    # Username from url
    username = request.args(0)
    
    # Find user in db
    user = db(db.auth_user.username == username).select().first()
    
    # Generate name to pass to page
    firstName = user.first_name
    lastName = user.last_name
    showLast = user.displayFullName
    personalName = firstName
    if showLast:
        personalName += ' ' + lastName
        
    # Get profile picture for page
    profilePicture = user.picture
    
    # Get quote
    personalQuote = user.personalQuote
    
    # Get posts
    posts = db((db.posts.recieverID == user.id) & (db.posts.approved == True)).select()
    
    # Get Relationships
    relationships = db(db.relationships.userID == user.id).select().first()
    
    # Get Friends
    friends = relationships.friends
    
    # Find Mutual Friends or Pending Friends
    mutualFriends = None
    pendingFriends = None
    if auth.user:
        if (auth.user.id == user.id):
            pendingFriends = relationships.pending
        else:
            viewerFriends = db(db.relationships.userID == auth.user).select().first().friends
            mutualFriends = set(friends) & set(viewerFriends)
    
    return dict(username = username, 
                 personalName = personalName, 
                 profilePicture = profilePicture, 
                 personalQuote = personalQuote, 
                 posts = posts, 
                 friends = friends, 
                 mutualFriends = mutualFriends,
                 pendingFriends = pendingFriends)

def new_post():
    messageBody = request.vars.your_message

    if not auth.user:
        response.flash = "You aren't logged in!"
        return
    
    if messageBody:
        recipient = db(db.auth_user.username == request.args(0)).select().first()
        ret = db.posts.validate_and_insert(senderID=auth.user.id, recieverID=recipient, body=messageBody, timePosted=datetime.utcnow())
        if ret.id:
            response.flash = "Successfully posted!"
        else:
            response.flash = "failed to post"

    return

def manual_login():
    username = request.vars.username;
    password = request.vars.password;
    user = auth.login_bare(username, password);
    if user == False:
        return "jQuery('#loginForm').hide();"
    else:
        return ""

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
