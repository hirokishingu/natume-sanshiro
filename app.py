from flask import Flask, render_template, request, redirect, url_for
from gensim.models import word2vec
import re
import os.path

app = Flask(__name__)

wakachigaki_file = "sanshiro.wakachi"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/post", methods=["GET", "POST"])
def post():
	if request.method == "POST":
		try:
			word = request.form["name"]
			data = word2vec.LineSentence(wakachigaki_file)
			model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
			name = model.most_similar(positive=[word])

		except:
			warn = ""
			if request.form["name"]:
				word = request.form["name"]
				warn = word + " 、は三四郎に関係ないみたいだね"
			return render_template("index.html", warn=warn)

		return render_template("index.html",
					name=name, word=word)
	else:
		return redirect(url_for("index"))

if __name__ == "__main__":
	app.debug = True
	app.run()

