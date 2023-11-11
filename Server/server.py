from flask import Flask, request, jsonify
import util
app = Flask(__name__)

@app.route('/get_data')
def get_data():
    town, flat_model, flat_type, storey_range, sales_month = util.get_categorical()
    response = jsonify({
        'town': town,
        'flat_model': flat_model,
        'storey_range': storey_range,
        'flat_type': flat_type,
        'sales_month': sales_month
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
@app.route('/predictor', methods = ['POST'])
def predictor():
    town = request.form['town']
    flat_type = request.form['flat_type']
    storey_range = request.form['storey_range']
    floor_area_sqm = float(request.form['floor_area_sqm'])
    flat_model = request.form['flat_model']
    lease_commence_date = int(request.form['lease_commence_date'])
    sales_year = int(request.form['sales_year'])
    sales_month = request.form['sales_month']

    response = jsonify({
        'resale_price' : util.get_estimated_price(town = town, flat_type = flat_type, storey_range = storey_range, floor_area_sqm = floor_area_sqm, flat_model= flat_model, lease_commence_date = lease_commence_date, sales_year = sales_year,sales_month = sales_month)
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



if __name__ == '__main__':
    print("Starting Flask Server")
    app.run()
