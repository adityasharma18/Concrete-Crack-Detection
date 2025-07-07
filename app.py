from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import base64

app = Flask(__name__)

model = tf.keras.models.load_model('model/concrete_crack_model.keras')

def predict_crack(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)[0][0]
    return "Crack Detected" if prediction >= 0.5 else "No Crack"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    show_graph = False  # default False

    if request.method == 'POST':
        # Camera capture
        if 'camera_image' in request.form:
            data_url = request.form['camera_image']
            header, encoded = data_url.split(",", 1)
            img_data = base64.b64decode(encoded)
            filepath = os.path.join('static', 'captured.png')
            with open(filepath, 'wb') as f:
                f.write(img_data)
            result = predict_crack(filepath)
            show_graph = True

        # File upload
        elif 'image' in request.files:
            file = request.files['image']
            if file:
                filepath = os.path.join('static', file.filename)
                file.save(filepath)
                result = predict_crack(filepath)
                show_graph = True

    return render_template('index.html', result=result, show_graph=show_graph)

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
