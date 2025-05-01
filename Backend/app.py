from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/test')
def test():
    return [
  {
    "_id": "6812eb7ab5c84bd4c4d5d414",
    "name": "Fernandez Franklin",
    "gender": "male",
    "company": "STOCKPOST"
  },
  {
    "_id": "6812eb7ab5ba613bbbfe4957",
    "name": "Lora Middleton",
    "gender": "female",
    "company": "PAPRICUT"
  },
  {
    "_id": "6812eb7aa902215c8436245a",
    "name": "Jennings Blankenship",
    "gender": "male",
    "company": "EQUICOM"
  },
  {
    "_id": "6812eb7a83f5f49c410d74a2",
    "name": "Kelley Frederick",
    "gender": "female",
    "company": "KNOWLYSIS"
  },
  {
    "_id": "6812eb7a51dde1459e1061af",
    "name": "Angelique Peterson",
    "gender": "female",
    "company": "SEALOUD"
  },
  {
    "_id": "6812eb7a7bc7d0b35655e5ca",
    "name": "Dejesus Austin",
    "gender": "male",
    "company": "GOGOL"
  },
  {
    "_id": "6812eb7ade2830023da19148",
    "name": "Therese Perez",
    "gender": "female",
    "company": "QABOOS"
  }
]


if __name__ == '__main__':
    app.run(debug=True)