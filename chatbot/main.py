from flask import Flask,render_template,request
from pymongo import MongoClient
import pickle,random
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
model = pickle.load(open('chatbot_data.pkl','rb'))
db = MongoClient("mongodb://localhost:27017/")["ml_api"]["chatbot"]


pattern = model["pattern"]
response_map = model["response_map"]
vector = model["vector"]
x = model["x"]
chat_history = []

def chat_response(user_input):
    user_vec = vector.transform([user_input])
    similarity = cosine_similarity(user_vec, x)
    idx = similarity.argmax()
    best_score = similarity[0][idx]

    if best_score < 0.5:
        
        return "Sorry, I can't understand you"

    match_pattern = pattern[idx]
    return random.choice(response_map[match_pattern])

@app.route('/',methods=['GET','POST'])
def chat():
    if request.method == 'POST':
        user_msg = request.form.get('message')
        if user_msg.strip():
            bot = chat_response(user_msg)
            chat_history.append({"role": "user", "text": user_msg})
            chat_history.append({"role": "bot", "text": bot})

    db.insert_one({'chat_history': chat_history})
    return render_template('index.html',chat_history=chat_history)

if __name__ == '__main__':
        app.run(debug=True)