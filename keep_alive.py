from flask import Flask, render_template
from threading import Thread
import random

app = Flask(""
#   __name__,
#   template_folder='templates',
#   static_folder='styles'
)


@app.route('/')
def main():
    # return render_template('index.html')
    return "Active"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()
