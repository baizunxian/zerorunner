from flask_cors import CORS
from flask_script import Manager

from autotest.app import create_app

app = create_app()
app.config['DEBUG'] = False
CORS(app, supports_credentials=True)
manager = Manager(app)

if __name__ == '__main__':
    app.run(debug=False, port=8012)
    # manager.run()
