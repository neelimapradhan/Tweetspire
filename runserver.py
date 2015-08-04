from flask import Flask
from flask import Flask, render_template
from app import sentiment

app = Flask(__name__)

@app.route("/")
def main():
	html_list = sentiment.getEmbed()
	return render_template('home.html', htmls = html_list[:5])

if __name__ == "__main__":
	app.run(debug=True)