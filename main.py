from flask import Flask, render_template, request, redirect, url_for
from forms import File, Column
import os
from werkzeug.utils import secure_filename
import pandas as pd
from plots import Barchart, PieChart, BoxPlot, HistPlot, DistPlot, ScatterPlot, Word_Cloud
app = Flask(__name__)
UPLOAD_FOLDER = "./Datasets"
app.config["SECRET_KEY"] = "abcd"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/", methods = ["POST", "GET"])
@app.route("/home", methods = ["POST", "GET"])
def home():
    form = File()
    if form.validate_on_submit():
        file = form.file.data
        if str(file.filename).split(".")[-1] not in ["csv", "json"]:
            error = "CSV files or JSON files only"
            return render_template("home.html", error = error, form = form)
        else:
            if str(file.filename).split(".")[-1] == "csv":
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename("Data" + str(len(os.listdir("./DataSets")) + 1) +".csv")))
                return redirect(url_for("analysis"))
            else:
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename("Data" + str(len(os.listdir("./DataSets")) + 1) +".json")))
                return redirect(url_for("analysis"))
    return render_template("home.html", form=form)




@app.route("/analysis", methods = ["POST", "GET"])
def analysis():
    df = pd.read_csv("./Datasets/Data" + str(len(os.listdir("./DataSets"))) + ".csv")
    if request.method == "POST":
        data = request.form.get('column_form')
        column = {"data" : data}
        return redirect(url_for('column', c=data, **column))
    return render_template("analysis.html", columns = df.columns, sum_null = df.isnull().sum(), types = df.dtypes)




@app.route("/column/<c>", methods = ["POST", "GET"])
def column(c):
    df = pd.read_csv("./Datasets/Data" + str(len(os.listdir("./DataSets"))) + ".csv")
    col = request.args.get("data")
    n = len(df[col].value_counts())
    m = len(df)
    if df[col].dtype == "object" and (n/m) > 0.5: 
        plot1 = Word_Cloud(df, col)
        return render_template("column.html", type = "Text Analysis", data = df[col], plots = plot1)
    elif df[col].dtype == "object" and (n/m) < 0.5:
        plot1 = PieChart(df, col)
        plot2 = Barchart(df, col)
        l = {"Pie Chart": plot1,
             "Bar Chart": plot2}
        return render_template("column.html", type = "Categorical Analysis", data = df[col], plots = l)
    elif df[col].dtype == "int64" or df[col].dtype == "float64":
        plot1 = HistPlot(df, col)
        plot2 = BoxPlot(df, col)
        plot3 = DistPlot(df, col)
        plot4 = ScatterPlot(df, col)
        desc = df.describe()
        l = {"Histogram": plot1,
             "Box Plot": plot2,
             "Distribution Plot" : plot3,
             "Scatter Plot" : plot4}
        df1 = df[df.columns[df.dtypes == "int64"]]
        print(df1.corr())
        return render_template("column.html", type = "Numerical Analysis", data = df[col], plots = l, desc = desc, columns=df.columns, corr = df1.corr()[col])
    return render_template("column.html", type = df[col].dtype)
if __name__ == "__main__":
    app.run(debug=True)
