from flask import Flask, render_template, request
from model import predict_crop, accuracy
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Profit data
crop_price = {
    "rice": 2000,
    "wheat": 1800,
    "maize": 1700,
    "cotton": 3000,
    "sugarcane": 2500,
    "banana": 3500,
    "mango": 4000,
    "apple": 5000,
    "grapes": 4500,
    "coffee": 3200,
    "lentil": 1500,
    "chickpea": 1600
}

@app.route('/')
def home():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temp = float(request.form['temp'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        if not (0 <= ph <= 14):
            return redirect(url_for('home', error="Invalid pH value (0–14 only)"))

        if rainfall < 0:
            return redirect(url_for('home', error="Rainfall cannot be negative"))
        input_data = [N, P, K, temp, humidity, ph, rainfall]

        crop = predict_crop(input_data)
        price = crop_price.get(crop)

        if price:
            profit = f"₹{price} (High Profit Crop)"
        else:
            profit = "Moderate Profit Crop"

# 🔹 RETURN RESULT
        return render_template('result.html',
                       crop=crop,
                       profit=profit,
                       acc=accuracy)

    except:
        return "Error in input data"

if __name__ == "__main__":
    app.run(debug=True)