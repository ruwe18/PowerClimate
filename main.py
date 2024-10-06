from flask import Flask, jsonify, send_from_directory
import pandas as pd

app = Flask(__name__)

# Load data
url = 'pilot_topdown_CO2_Budget_countries_v1.csv'
df_all = pd.read_csv(url, skiprows=52)
alpha_3_codes = df_all['Alpha 3 Code'].unique()

years_of_interest = [2015, 2016, 2017, 2018, 2019, 2020]

dict_all_years_data = {}

# Process data for each year
for year in years_of_interest:
    
    dict_country_data = {'sum_totalFF': 0}
    
    # Iterate over each Alpha 3 code
    for country_code in alpha_3_codes:
        # Check if the code has exactly 3 letters
        if len(country_code) == 3:
            country_data = df_all[(df_all['Alpha 3 Code'] == country_code) & (df_all['Year'] == str(year))]
    
            # Check if data is available
            if not country_data.empty:
                emissions = country_data["FF (TgCO2)"].values[0]
                dict_country_data[country_code] = {"FF": emissions}  
                dict_country_data['sum_totalFF'] += emissions  
    
    # Calculate percentages for each country
    for country_code in dict_country_data:
        if country_code != 'sum_totalFF':  
            dict_country_data[country_code]["porcentagemFF"] = (dict_country_data[country_code]["FF"] / dict_country_data['sum_totalFF']) * 100
            
    dict_all_years_data[year] = dict_country_data
    
@app.route('/dados', methods=['GET'])
def get_emissions():
    return jsonify(dict_all_years_data)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')  # Página inicial servindo index.html

@app.route('/main')
def main():
    return send_from_directory('', 'main.html')  # Página acessando main.html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)