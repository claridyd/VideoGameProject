from flask import Flask, render_template,request, jsonify
import plotly
import plotly.graph_objs as go
import json
import tablib
import os
import pandas as pd
######Added by Claridy
# from config import password
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask_sqlalchemy import SQLAlchemy
######

app = Flask(__name__)
##########################################
# Database Setup 
# Claridy 10/14/19
###########################################

# DB_URL = 'postgresql+psycopg2://postgres:'+ password + '@localhost:5432/videogames_db'
DB_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)
#Save reference to table
Games = Base.classes.games

# stmt = db.session.query(Games).statement
session = Session(db.engine)
df2 = pd.read_sql_query('SELECT * FROM Games', session.bind)
print(df2)
##################################
# save df2 as data_html # dc add
data_html = df2.to_html
#############################################
# dataset = tablib.Dataset()        removed by Claridy
# with open(os.path.join(os.path.dirname(__file__),'vgsales.csv')) as f:
#     dataset.csv = f.read()

# df = pd.read_csv('vgsales.csv')       removed by Claridy

###updated df below to df2 to use database by Claridy
def create_plot(feature):
    if feature == 'Bar':
        data = [go.Bar(
            x = df2["Genre"].values.tolist(), 
            y = df2["NA_Sales"].values.tolist(),
            name='NA Sales'
        )]
    elif feature == 'Bar2':
        data = [go.Bar(
            x = df2["Genre"].values.tolist(), 
            y = df2["PAL_Sales"].values.tolist(),
            name='PAL Sales',
            marker=dict(
                color='rgb(255,127,14,255)',
            )
        )]
    elif feature == 'Bar3':
        data = [go.Bar(
        x = df2["Genre"].values.tolist(), 
        y = df2["JP_Sales"].values.tolist(), 
        name='Japan Sales',
        marker=dict(
            color='rgb(44,160,44,255)',
        )
    )]
    elif feature == 'Bar4':
        data= [go.Bar(
            x = df2["Genre"].values.tolist(), 
            y = df2["Other_Sales"].values.tolist(),
            name='Other Sales',
            marker=dict(
                color='rgb(214,39,40,255)',
        )
    )]
    else:
        data = [go.Bar(
            x = df2["Genre"].values.tolist(), 
            y = df2["Global_Sales"].values.tolist(), 
            name='Global Sales',
            marker=dict(
                color='rgb(148,53,193,255)',
        )
    )]


    layout = go.Layout(
        title='Video Game Sales in 2018',
        xaxis=dict(
            title="Genre",
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        yaxis=dict(
            title='USD (millions)',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        barmode='group',
    )
    fig = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/')
def index():
    feature = 'Bar'
    bar = create_plot(feature)
    #data = dataset.html             #where does dataset.html come from
    #data2 = df2.to_html
    #return dataset.html
    #return render_template('index.html', plot=bar, data=data)
    return render_template('index.html', plot=bar, tables=[df2.to_html(classes='data', header='true')])

@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON = create_plot(feature)


    return graphJSON


if __name__ == '__main__':
    app.run(debug=True)
