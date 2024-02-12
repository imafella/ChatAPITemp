# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from Tools.PrefixMiddleware import PrefixMiddleware
from Routes.user import user_bp
from Routes.chat import chat_bp
from Routes.message import message_bp
from Routes.reaction import reaction_bp


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.debug = True
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/api/v1')
app.register_blueprint(user_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(message_bp)
app.register_blueprint(reaction_bp)



# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'


@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name


# this route will test the database connection - and nothing more
# @app.route('/')
# def testdb():
#     try:
#         db.session.query(text('1')).from_statement(text('SELECT 1')).all()
#         return '<h1>It works.</h1>'
#     except Exception as e:
#         # e holds description of the error
#         error_text = "<p>The error:<br>" + str(e) + "</p>"
#         hed = '<h1>Something is broken.</h1>'
#         return hed + error_text


# main driver function
if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
