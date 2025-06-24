from flask import Flask, render_template, redirect, request, session, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from onelogin.saml2.auth import OneLogin_Saml2_Auth
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Helper to prepare request for python3-saml
def prepare_flask_request(req):
    return {
        'https': 'on',
        'http_host': req.host,
        'script_name': req.path,
        'server_port': req.environ.get('SERVER_PORT'),
        'get_data': req.args.copy(),
        'post_data': req.form.copy()
    }

def init_saml_auth(req):
    return OneLogin_Saml2_Auth(req, custom_base_path='saml')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route('/saml/acs', methods=['POST'])
def acs():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    auth.process_response()
    errors = auth.get_errors()
    if len(errors) == 0:
        session['user_info'] = auth.get_attributes()
        return redirect(url_for('dashboard'))
    return f"Login failed: {errors}", 401

@app.route('/dashboard')
def dashboard():
    user_info = session.get('user_info')
    if not user_info:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=user_info)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/saml/metadata/')
def metadata():
    from onelogin.saml2.metadata import OneLogin_Saml2_Metadata
    from onelogin.saml2.settings import OneLogin_Saml2_Settings

    settings = OneLogin_Saml2_Settings(custom_base_path='saml', sp_validation_only=True)
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)
    if len(errors) > 0:
        return f"Error in metadata: {errors}", 500
    return metadata, {'Content-Type': 'text/xml'}

if __name__ == '__main__':
    app.run(debug=True)
