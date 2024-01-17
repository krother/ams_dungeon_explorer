
from flask import Flask, render_template
import requests  # pip install requests


app = Flask(__name__)

@app.route("/on")  # connects a browser URL to this function
def car_on():
    # question: what protocol does the Arduino wifi adapter understand?
    # answers: HTTP
    # example HTTP request to some computer on the web
    url = "http://www.academis.eu/advanced_python"  # put the ip of the arduino Wifi here
    result = requests.get(url)
    print(result.status_code)
    print(result.text[:100])
    return render_template('test.html', message="Now the car is on")

@app.route("/off")  # @ is called a decorator
def car_off():
    return render_template('test.html', message="Now the car is off")


@app.route("/")
def main():
    return render_template('test.html',
              title='Start page',
              animals=['cat', 'dog', 'fish', 'platypus']
              )


if __name__ == "__main__":
    app.run()
