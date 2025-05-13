from flask import Flask, render_template, request, redirect, url_for
import os, json, csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    with open('katalog_data.json', 'r') as f:
        katalog = json.load(f)
    return render_template('index.html', katalog=katalog)

@app.route('/pesan', methods=['POST'])
def pesan():
    nama = request.form['nama']
    layanan = request.form['layanan']
    pesan = request.form['pesan']
    with open('pesanan.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nama, layanan, pesan])
    return redirect('/')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        kategori = request.form['kategori'].lower()
        file = request.files['gambar']
        if file:
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            with open('katalog_data.json', 'r+') as f:
                data = json.load(f)
                if kategori not in data:
                    data[kategori] = []
                data[kategori].append(filename)
                f.seek(0)
                json.dump(data, f, indent=2)
        return redirect('/upload')
    return '''
    <h2>Upload Gambar Katalog (Admin)</h2>
    <form method="POST" enctype="multipart/form-data">
      <input type="text" name="kategori" placeholder="Kategori (sofa, kursi, etc)" required><br><br>
      <input type="file" name="gambar" required><br><br>
      <button type="submit">Upload</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)