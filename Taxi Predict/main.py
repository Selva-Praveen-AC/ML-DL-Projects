from flask import Flask,request,render_template,jsonify
import numpy as np
import pickle
from flask_pymongo import PyMongo

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

app.config['MONGO_URI'] = 'mongodb://localhost:27017/taxi_predict'
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        input_data = [int(i) for i in request.form.values()]
        final_value = np.array(input_data).reshape(1,-1)
        prediction = model.predict(final_value)
        output = round(prediction[0],2)
        
        db.taxi_predict.insert_one({'Priceperweek':input_data[0],
                                    'Population':input_data[1],
                                    'Monthlyincome':input_data[2],
                                    'Averageparkingpermonth':input_data[3],
                                    'Predictedfare':output})
        return render_template('index.html', prediction_text='The predicted fare is {}'.format(output))
    
@app.route('/api',methods=['POST'])
def api_read():
    if request.method == 'POST':
        input_data = request.get_json()
        final_value = np.array([input_data['Priceperweek'],
                                input_data['Population'],
                                input_data['Monthlyincome'],
                                input_data['Averageparkingpermonth']]).reshape(1,-1)
        prediction = model.predict(final_value)
        output = round(prediction[0],2)
        db.taxi_predict.insert_one({'Priceperweek':input_data['Priceperweek'],
                                    'Population':input_data['Population'],
                                    'Monthlyincome':input_data['Monthlyincome'],
                                    'Averageparkingpermonth':input_data['Averageparkingpermonth'],
                                    'Predictedfare':output})
        return jsonify({"Status":"Success","Predicted fair": output })  
if __name__ == "__main__":
    app.run(debug=True)