"""
Main module of the server file
"""

from flask import render_template
import connexion

HOST = '127.0.0.1'
PORT = 5001

app = connexion.App(__name__, specification_dir="../")
app.add_api("server/swagger.yml")


# create default URL route
@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host = HOST, port = PORT, debug=True)
