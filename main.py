from flask import Flask, render_template, request, jsonify
from dictionary import printer
import alphaTextToBraille, brailleTextToAlpha
from PredictBraille import PredictBraille
from sys import argv
import pytesseract 
from PIL import Image
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
app.secret_key = 'this is a very secure string'
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/learnbraille')
def learnbraille():
    return render_template('learnbraille.html')

@app.route('/engtext2braille', methods=['POST'])
def eng_text_to_braille():
    return render_template('engtext2braille.html')

@app.route('/engimg2braille', methods=['POST'])
def eng_img_to_braille():
    return render_template('engimg2braille.html')

@app.route('/brailletext2eng', methods=['POST'])
def braille_text_to_eng():
    return render_template('brailletext2eng.html')

@app.route('/brailleimg2eng', methods=['POST'])
def braille_img_to_eng():
    return render_template('brailleimg2eng.html')

@app.route('/translateengtext1', methods=['POST'])
def translate_engtext_grade1():
    braille_input = request.form.get('textInput')
    translation_result = alphaTextToBraille.translate(braille_input,1)
    return jsonify({'result': translation_result})

@app.route('/translateengtext2', methods=['POST'])
def translate_engtext_grade2():
    braille_input = request.form.get('textInput')
    translation_result = alphaTextToBraille.translate(braille_input,2)
    return jsonify({'result': translation_result})

@app.route('/translatebrailletext',methods=['POST'])
def translate_brailletext():
    print("Braille Translation")
    braille_input = request.form.get('textInput')
    result=brailleTextToAlpha.translate(braille_input)
    return jsonify({'result': result})

@app.route('/engImageTranslate', methods=['POST'])
def engImageTranslate():
    if 'image' in request.files:
        uploaded_image = request.files['image']
        image_path = 'temp_image.png'   # Save the uploaded image to a temporary file
        uploaded_image.save(image_path)
        # Perform OCR on the uploaded image
        braille_image = Image.open(image_path)
        braille_text = pytesseract.image_to_string(braille_image)
        return jsonify({'result': braille_text})
    else:
        return jsonify({'error': 'No image file provided.'})

@app.route('/brailleImageTranslate', methods=['POST'])
def brailleImageTranslate():
    if 'image' in request.files:
        uploaded_image = request.files['image']
        image_path = 'temp_image.png'  # Save the uploaded image to a temporary file
        uploaded_image.save(image_path)
        # Perform OCR on the uploaded image
        predictor = PredictBraille()
        result = predictor.predict(image_path)
        return jsonify({'result': result})
    else:
        return jsonify({'error': 'No image file provided.'})

if __name__ == '__main__':
    app.run(debug=True)