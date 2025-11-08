from flask import Flask,request,jsonify,render_template
import pickle,pandas as pd
from pymongo import MongoClient

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))
db = MongoClient("mongodb://localhost:27017/")["ml_api"]["api"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    input_data =request.get_json()
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    result = "Heart Disease Present" if prediction==1 else "No Heart Disease"
    db.insert_one({'input':input_data,
        'prediction':int(prediction),
                    'result':result})
    return jsonify({'input':input_data,
        'prediction':int(prediction),
                    'result':result})

if __name__ == '__main__':
    app.run(debug=True)