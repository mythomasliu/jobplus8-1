
from flask import Flask, render_template, url_for
from .config import configs

def create_app(config):
	app = Flask(__name__)
	app.config.from_object(configs.get(config))

	@app.route('/test')
	def test():
		return render_template('index.html')

	return app
