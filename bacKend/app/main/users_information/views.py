from .. import main

@main.route('/usersinformation', methods=['GET','POST'])
def index():
    return 'This is index'