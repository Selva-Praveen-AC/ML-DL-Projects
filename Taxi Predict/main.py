from flask import Flask,request,render_template
import numpy as np
import pickle
from 

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

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
        return render_template('index.html', prediction_text='The predicted fare is {}'.format(output))
    
if __name__ == "__main__":
    app.run(debug=True)