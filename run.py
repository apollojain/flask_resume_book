import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug import secure_filename

UPLOAD_FOLDER = 'resumes'
ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx'])

app = Flask(__name__)
app.secret_key = 'some_secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploaded_file/', methods=['GET'])
def uploaded_file():
	return "hello"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.dirname(os.path.realpath(__file__))
            lst = os.listdir(path + "/resumes")
            print(filename)
            print(lst)
            if filename in lst:
                i = 2
                placeholder = filename.rsplit('.', 1)[0]
                newfilename = placeholder + "_" + str(i) + ".pdf"
                while newfilename in lst:
                    i+= 1
                    newfilename = placeholder + "_" + str(i) + ".pdf"
                filename = newfilename                         
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File uploaded successfully!")
                
        else:
            flash("Please upload a file of type .doc, .docx, or .pdf")
        return redirect(url_for('upload_file'))
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug = True)