import tensorflow as tf
model = tf.keras.models.load_model('models/hurricane_alt.keras')

from flask import Flask, request
import numpy as np

app = Flask(__name__)

@app.route('/models/hurricane_damage/v1', methods=['GET'])
def model_info():
   return {
      "version": "v1",
      "name": "hurricane_damage",
      "description": "Classify images containing buildings after a hurricane (damaged or not damaged)",
      "number_of_parameters": 2601153
   }

@app.route('/models/hurricane_damage/v1', methods=['POST'])
def classify_clothes_image():
   im = request.json.get('image')
   if not im:
      return {"error": "The `image` field is required"}, 404
   try:
      data = preprocess_input(im)
   except Exception as e:
      return {"error": f"Could not process the `image` field; details: {e}"}, 404
   result = model.predict([data]).tolist()[0][0]
   if result < 0.5:
      return {"result": "contains damage"}
   else:
      return {"result": "contains no damage"}

def preprocess_input(im):
   """
   Converts user-provided input into an array that can be used with the model.
   This function could raise an exception.
   """
   # convert to a numpy array and rescale
   d = np.array(im) / 255.0

   # then add an extra dimension
   return d.reshape(1, 128, 128, 3)

# start the development server
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')