from flask import Flask, request
import os

app = Flask(__name__)

# Set the paths for our makeshift database and upload directory
user_info_path = "my_sql_temp_user_info/users.txt"
upload_path = "my_sql_temp_data"

logged_in = False
@app.route('/')
@app.route('/login', methods=['POST'])
def login():
    global logged_in
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the user exists in our "database" (text file in this case)
    with open(user_info_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            stored_username, stored_password = line.strip().split(":")
            if stored_username == username and stored_password == password:
                logged_in = True
                return "Logged in successfully"
    return "Invalid credentials", 401

@app.route('/upload', methods=['POST'])
def upload_file():
    global logged_in
    if not logged_in:
        return "Unauthorized", 401

    uploaded_file = request.files.get('file')
    if uploaded_file:
        filename = os.path.join(upload_path, uploaded_file.filename)
        uploaded_file.save(filename)
        return f"File uploaded successfully as {filename}"
    return "No file uploaded", 400

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    if not os.path.exists("my_sql_temp_user_info"):
        os.makedirs("my_sql_temp_user_info")
    
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    app.run(debug=True)
