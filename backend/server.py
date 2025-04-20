from flask import Flask
import datetime

time = datetime.datetime.now()

# start flask
app = Flask(__name__)

# route for data
@app.route('/data')

def getTime():

    #return an api to show in reactjs
    return {
        'Name':"pl4nt", 
        "Species":"human?",
        "Date":time, 
        "programming":"python"
        }

# Running app
if __name__ == '__main__':
    app.run(debug=True)