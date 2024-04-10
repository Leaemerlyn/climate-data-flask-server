import base64
from io import BytesIO
from flask import Flask, request, render_template, session, redirect, make_response
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
#from flask_cors import CORS, cross_origin

app = Flask(__name__)
#cors = CORS(app)

#app.config['CORS_HEADERS'] = 'Content-Type'
matplotlib.use('agg')

print('~~~The server started!~~~')

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def html_table():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()

    print(request.json)

    img = BytesIO()
    df = pd.read_csv('./mysite/climate.csv')
    climate_year_df_test = df[is_selected_country(df["country"], request.json)]
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=climate_year_df_test, x='year', y='avg_temp', hue="country")
    plt.title('test')
    plt.xlabel('Year')
    plt.ylabel('temp')
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('ascii')
    return _corsify_actual_response(make_response(plot_url))

    # return render_template("simple.html", plot_url=plot_url)

    # return render_template('simple.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

def _build_cors_preflight_response():
    print("The options method was called!")
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def is_selected_country(df_series, countries):
    df_list = df_series.to_list()
    return [is_selected_country_helper(df_item, countries) for df_item in df_list]
    

def is_selected_country_helper(df_item, countries):
    for country in countries:
        if df_item == country:
            return True
        
    return False


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')