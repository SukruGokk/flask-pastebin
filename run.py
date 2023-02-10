from flask import Flask, render_template, request
from flask_lt import run_with_lt # public host
import random
import string
import json

def get_key(letters_count, digits_count):
	letters = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
	digits = ''.join((random.choice(string.digits) for i in range(digits_count)))

	# Convert resultant string to list and shuffle it to mix letters and digits
	sample_list = list(letters + digits)
	random.shuffle(sample_list)
	# convert list to string
	final_string = ''.join(sample_list)
	return(final_string)

app = Flask(__name__)
run_with_lt(app)

@app.route("/", methods = ['GET'])
def index():
	return render_template('index.html')

@app.route('/get')
def get_route():
	key = request.args.get('key')

	link = '{}get?key={}'.format(request.url_root, key)

	with open("data.json", "r") as file:
		json_data = json.loads(file.read())

	if(key in json_data.keys()):
		return render_template('paste.html', data = json_data[key], link = link)
	else: # if paste doesnt exist
		return render_template('not_found.html')

@app.route('/info')
def info():
	return render_template('info.html')

@app.route('/create-paste', methods=['POST'])
def create_paste():
	key = get_key(5, 0)
	link = '{}get?key={}'.format(request.url_root, key)


	with open("data.json", "r") as file:
		json_data = json.load(file)

	json_data[key] = {'author': request.form['author'], 'title': request.form['title'], 'text': request.form['text']}

	with open("data.json", "w") as file:
		json.dump(json_data, file)

	return render_template('paste.html', data = json_data[key], link = link)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('not_found.html')

if __name__ == '__main__':
	app.run()
