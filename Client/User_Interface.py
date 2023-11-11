import streamlit as st
import requests

# Function to get data from the Flask server
def get_data():
    url = 'http://127.0.0.1:5000/get_data'  # Replace with your Flask server URL
    response = requests.get(url)
    data = response.json()
    return data

# Function to make predictions using the Flask server
def predict(town, flat_type, storey_range, floor_area_sqm, flat_model, lease_commence_date, sales_year, sales_month):
    url = 'http://127.0.0.1:5000/predictor'  # Replace with your Flask server URL
    data = {
        'town': town,
        'flat_type': flat_type,
        'storey_range': storey_range,
        'floor_area_sqm': floor_area_sqm,
        'flat_model': flat_model,
        'lease_commence_date': lease_commence_date,
        'sales_year': sales_year,
        'sales_month': sales_month
    }
    response = requests.post(url, data=data)
    result = response.json()
    return result['resale_price']

# Streamlit App



if __name__ == '__main__':
    st.title('Singapore House Resale Price Prediction'.upper())

    # Get data from Flask server
    data = get_data()


    # Input form for predictions
    with st.form("Make Prediction"):
        column1, column2 = st.columns(2)
        col1, col2 = st.columns(2)
        with column1:
            town = st.selectbox('Town', data['town'])
            flat_type = st.selectbox('Flat Type', data['flat_type'])
            storey_range = st.selectbox('Storey Range', data['storey_range'])
            flat_model = st.selectbox('Flat Model', data['flat_model'])
        with column2:
            floor_area_sqm = st.number_input('Floor Area (sqm)', min_value=0.0, value=50.0)
            lease_commence_date = st.number_input('Lease Commence Date', min_value=1960, value=1980)
        with col1:
            sales_month = st.selectbox('Sales Month', data['sales_month'])
        with col2:
            sales_year = st.number_input('Sales Year', min_value=2000, value=2022)
        submit_button = st.form_submit_button("Predict")

        if submit_button:
            predicted_price = predict(town, flat_type, storey_range, floor_area_sqm, flat_model, lease_commence_date,
                                      sales_year, sales_month)
            st.success(f'Predicted Resale Price: {predicted_price} S$')




