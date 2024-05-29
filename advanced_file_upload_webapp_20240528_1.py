# 导入 Flask 模块中的 Flask 类，用于创建 Flask 应用
from flask import Flask, render_template, request, redirect, url_for, flash, session
# 导入 Werkzeug 模块中的一些实用工具，用于处理文件和密码
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
# 导入 os 模块，用于与操作系统交互
import os

# 创建一个 Flask 应用实例，这个实例是整个应用的核心
app = Flask(__name__)

# 设置一个密钥，用于加密会话数据
app.secret_key = 'supersecretkey'

# 配置文件上传的文件夹，所有上传的文件都会存储在这个文件夹里
app.config['UPLOAD_FOLDER'] = 'uploads'

# 设置上传文件的最大尺寸为 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# 模拟用户数据，这里我们创建一个字典，包含一个用户和加密后的密码
users = {
    "admin": generate_password_hash("password123")
}

# 定义允许上传的文件扩展名
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# 定义一个函数，用于检查文件扩展名是否允许
def allowed_file(filename):
    # 检查文件名中是否包含点，且点后面的扩展名是否在允许列表中
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 定义路由，当用户访问网站根目录（/）时，执行这个函数
@app.route('/')
def index():
    # 检查用户是否已登录
    if 'username' in session:
        # 获取上传文件夹中的所有文件
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        # 渲染 index.html 模板，并传递文件列表
        return render_template('index.html', files=files)
    # 如果用户未登录，重定向到登录页面
    return redirect(url_for('login'))

# 定义路由，当用户访问 /login 时，执行这个函数
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取用户提交的用户名和密码
        username = request.form['username']
        password = request.form['password']
        # 检查用户名和密码是否正确
        if username in users and check_password_hash(users[username], password):
            # 将用户名存储在会话中，表示用户已登录
            session['username'] = username
            # 重定向到主页
            return redirect(url_for('index'))
        # 如果用户名或密码错误，显示错误信息
        flash('Invalid credentials')
    # 渲染 login.html 模板
    return render_template('login.html')

# 定义路由，当用户访问 /logout 时，执行这个函数
@app.route('/logout')
def logout():
    # 从会话中删除用户名，表示用户已登出
    session.pop('username', None)
    # 重定向到登录页面
    return redirect(url_for('login'))

# 定义路由，当用户访问 /upload 时，执行这个函数
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # 检查用户是否已登录
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # 检查用户是否选择了文件
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # 检查文件是否符合允许的扩展名
        if file and allowed_file(file.filename):
            # 安全地获取文件名，防止目录遍历攻击
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # 检查文件是否已经存在
            if os.path.exists(filepath):
                flash('File already exists')
                return redirect(request.url)

            # 保存文件到上传文件夹
            file.save(filepath)
            flash('File successfully uploaded')
            # 渲染 upload_result.html 模板，并传递文件名
            return render_template('upload_result.html', filename=filename)

    # 渲染 upload.html 模板
    return render_template('upload.html')

# 检查 uploads 文件夹是否存在，如果不存在则创建它
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    # 以调试模式运行 Flask 应用
    app.run(debug=True)
