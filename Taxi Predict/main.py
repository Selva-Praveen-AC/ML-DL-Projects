from flask import Flask, render_template,request
import numpy as np
import pickle
import math


app= Flask(__name__)
model=pickle.load(open('model.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])

def predict():
    if request.method=='POST':
        input_data=[int (i) for i in request.form.values()]
        final=np.array(input_data).reshape(1,-1)
        f_predict=model.predict(final)
        output=round(f_predict[0],2)
        return render_template('index.html', prediction_text='The predicted value is {}'.format(math.floor(output)))


if __name__ == '__main__':
    app.run(debug=True)