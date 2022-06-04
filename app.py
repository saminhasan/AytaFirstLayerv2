#!/usr/bin/env python3
from flask import Flask
from flask_restful import Resource, Api

from recorder import Recorder

app = Flask(__name__)
api = Api(app)
r = Recorder()

class Fitness(Resource):
    def get(self, btn_id):
        if btn_id=='start':
            return r.start()
        elif btn_id=='stop':
            return r.stop()
        else:
            return {'error': 'Invalid button id'}

    # def post(self, btn_id):
    #     buttonInfo[btn_id] = request.form['data']
    #     return {btn_id: buttonInfo[btn_id]}

api.add_resource(Fitness, '/<string:btn_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

#curl http://localhost:5000/todo1 -d "data=Remember the milk" -X POST