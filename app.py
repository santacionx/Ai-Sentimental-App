from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient('mongodb+srv://sqn:123@cluster0.ttwwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['sentiment_analysis_db']  # Database name

# Define the collection
collection = db['sentiments']  # Collection name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Perform sentiment analysis
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    # Determine sentiment category based on polarity
    if polarity > 0.5:
        sentiment = 'Positive'
    elif 0.1 <= polarity <= 0.5:
        sentiment = 'Neutral'
    elif -0.1 < polarity < 0.1:
        sentiment = 'Neutral'
    elif -0.5 <= polarity <= -0.1:
        sentiment = 'Bad'
    elif polarity < -0.5:
        sentiment = 'Worst'
    else:
        sentiment = 'Unknown'

    # Store the text and sentiment analysis in MongoDB
    collection.insert_one({
        'text': text,
        'sentiment': sentiment,
        'polarity': polarity,
        'subjectivity': analysis.sentiment.subjectivity
    })

    return jsonify({
        'sentiment': sentiment,
        'polarity': polarity,
        'subjectivity': analysis.sentiment.subjectivity
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
