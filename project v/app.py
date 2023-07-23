import os
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_graph(data, graph_type):
    if graph_type == 'Pie':
        plt.figure(figsize=(8, 8))
        data.dropna(subset=[data.columns[-1]], inplace=True)
        data_numeric = data.iloc[:, -1].apply(pd.to_numeric, errors='coerce')
        data_numeric.dropna(inplace=True)
        plt.pie(data_numeric, labels=data_numeric.index, autopct='%1.1f%%')
        plt.title('Pie Chart')
        graph_file = os.path.join(app.config['UPLOAD_FOLDER'], 'pie_graph.png')
        plt.savefig(graph_file)
        plt.close()  # Close the plot to release resources
        return graph_file
    elif graph_type == 'Bar':
        plt.figure(figsize=(10, 6))
        data.dropna(subset=[data.columns[-1]], inplace=True)
        data_numeric = data.iloc[:, -1].apply(pd.to_numeric, errors='coerce')
        data_numeric.dropna(inplace=True)
        data_numeric.plot(kind='bar')
        plt.title('Bar Graph')
        graph_file = os.path.join(app.config['UPLOAD_FOLDER'], 'bar_graph.png')
        plt.savefig(graph_file)
        plt.close()  # Close the plot to release resources
        return graph_file
    elif graph_type == 'Line':
        plt.figure(figsize=(10, 6))
        data.dropna(subset=[data.columns[-1]], inplace=True)
        data_numeric = data.iloc[:, -1].apply(pd.to_numeric, errors='coerce')
        data_numeric.dropna(inplace=True)
        data_numeric.plot(kind='line', marker='o', color='b')
        plt.title('Line Graph')
        graph_file = os.path.join(app.config['UPLOAD_FOLDER'], 'line_graph.png')
        plt.savefig(graph_file)
        plt.close()  # Close the plot to release resources
        return graph_file
    elif graph_type == 'Scatter':
        plt.figure(figsize=(10, 6))
        data.dropna(subset=[data.columns[-1]], inplace=True)
        x_col = data.columns[-2]  # Assuming x-axis data is in the second-to-last column
        y_col = data.columns[-1]  # Assuming y-axis data is in the last column
        plt.scatter(data[x_col], data[y_col])
        plt.title('Scatter Plot')
        graph_file = os.path.join(app.config['UPLOAD_FOLDER'], 'scatter_plot.png')
        plt.savefig(graph_file)
        plt.close()  # Close the plot to release resources
        return graph_file
    else:
        raise ValueError('Invalid graph type')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        graph_type = request.form['graph_type']


        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename)) if filename.endswith('.csv') \
                else pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            graph_file = generate_graph(data, graph_type)

            return redirect(url_for('display_graph', graph_file=graph_file.replace('\\', '/')))
        else:
            return "Invalid file type. Please upload a CSV or Excel file."

    return render_template('index.html')


@app.route('/display')
def display_graph():
    graph_file = request.args.get('graph_file')
    if graph_file:
        return send_file(graph_file, mimetype='image/png')
    else:
        return "No graph file found."
@app.route('/line_graph', methods=['POST'])
def draw_line_graph():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename)) if filename.endswith('.csv') \
            else pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        graph_file = generate_graph(data, 'line')

        return redirect(url_for('display_graph', graph_file=graph_file.replace('\\', '/')))
    else:
        return "Invalid file type. Please upload a CSV or Excel file."

if __name__ == '__main__':
    
    app.run(debug=True)
