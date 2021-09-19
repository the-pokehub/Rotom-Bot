from flask import Flask
from threading import Thread

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
