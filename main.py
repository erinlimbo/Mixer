from flask import Flask, render_template

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "musicmixer",
})

db = firestore.client()

@app.route('/home')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.

    name = "Wagon Wheel"
    id = 12325
    artist = "Darius Rucker"

    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })

    doc_ref = db.collection(u'users').document(u'aturing')
    doc_ref.set({
        u'first': u'Alan',
        u'middle': u'Mathison',
        u'last': u'Turing',
        u'born': 1912
    })

    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

    return render_template('home.html', name=name, id=id, artist=artist)

@app.route('/profile')
def profile():

    return render_template('profile.html')

@app.route('/login')
def login():

    return render_template('login.html')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
