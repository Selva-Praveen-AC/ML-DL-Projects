from flask import Flask, request, jsonify,render_template
import pickle,numpy as np
from flask_pymongo import PyMongo

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

app.config['MONGO_URI'] = 'mongodb://localhost:27017/api'
mongo = PyMongo(app)
db= mongo.db

@app.route('/',methods=['GET'])
def student():
        return render_template('index.html')

@app.route('/student',methods=['POST'])
def set_student():
        hour = request.json.get('hour')
        if hour is None:
            return jsonify({'error': 'No hour provided'}), 400
        try:
            hour=float(hour)
            prediction = float(model.predict(np.array([[hour]]))[0])
            result = {'prediction': prediction}
            db.students.insert_one({'hour': hour, 'prediction': prediction})
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)