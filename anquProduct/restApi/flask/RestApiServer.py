#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-08-05


#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

def A(num1,num2):
	print "My first Rest API"
	return num1+num2

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
        # 'fun':A(1,1)
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/', methods=['GET'])
def get_tasks():
	# print "My first rest API"
    return jsonify({'answer': A(1,1)})

if __name__ == '__main__':
    app.run(debug=True)