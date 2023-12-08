#-----/Packages and imporsts imported/-----
import os 
from app import create_app, db
from app.models import People
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
#-----/App configuration started and app starts/-----
app = create_app(os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)
mail = Mail(app)
CORS(app)


#-----/Registering the function as a shell context function/-----
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, People=People)

#-----/This command starts the test functionality/-----
@app.cli.command()
def test():
    """Run the unit test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    