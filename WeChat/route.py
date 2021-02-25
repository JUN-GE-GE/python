from flask import render_template,redirect,url_for,request,abort,current_app,flash

from WeChat.forms import LoginForm,RegisterForm,EditProfileForm,ChatForm,PasswordResetRequestForm,PasswordResetForm
from flask_login import login_user, current_user,logout_user,login_required
from WeChat.models.user import User
from WeChat import db
from WeChat.models.chat import Chat
from WeChat.email import send_email
@login_required
def index():
    form = ChatForm()
    if form.validate_on_submit():
        c = Chat(body=form.chat.data, author=current_user)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('index'))
    page_num = int(request.args.get('page') or 1)
    chats = current_user.own_and_followed_chats().paginate(page=page_num,per_page=current_app.config['CHAT_PER_PAGE'], error_out=False)
    next_url = url_for('index',page=chats.next_num) if chats.has_next else None
    prev_url = url_for('index',page=chats.prev_num) if chats.has_prev else None
    return render_template('index.html', chats=chats.items, form=form, next_url=next_url, prev_url=prev_url)



def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form =LoginForm()
    if form.validate_on_submit():
        # msg = "username={},password={},remember_me={}".format(
        #     form.username.data,
        #     form.password.data,
        #     form.remember_me.data                             
        # )
        # print(msg)
        # 登录测试
        u = User.query.filter_by(username=form.username.data).first()
        if u is None or not u.check_password(form.password.data):
            print('Invalid username or password')
            return redirect(url_for('login'))
        login_user(u, remember=form.remember_me.data)    
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign In',form=form)   
def logout():
    logout_user()
    return redirect(url_for('login'))  

def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        # 判断是福哦已经登录
    form = RegisterForm()
    # 初始化一个form
    if form.validate_on_submit():#如果合法
        user = User(username= form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form = form,title='Registration')

@login_required
def user(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
         abort(404)
    page_num = int(request.args.get('page') or 1)     
    chats = u.chats.order_by(Chat.create_time.desc()).paginate(
        page=page_num,
        per_page=current_app.config['CHAT_PER_PAGE'],
        error_out=False
        )
    next_url = url_for(
        'Profile',
        page=chats.next_num,
        username=username) if chats.has_next else None
    prev_url = url_for(
        'Profile',
        page=chats.prev_num,
        username=username) if chats.has_prev else None
       
    if request.method == 'POST':
        if request.form['request_button'] == 'Follow':
            current_user.follow(u)
            db.session.commit()
        else:
            current_user.unfollow(u)
            db.session.commit()

    return render_template('user.html', title='Profile', chats=chats.items, user=u, next_url=next_url, prev_url=prev_url)
def page_not_found(e):
    return render_template('404.html'), 404

@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'GET':
        form.about_me.data = current_user.about_me
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('Profile', username=current_user.username))
    return render_template('edit_profile.html',form=form)

def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(
                "You should soon receive an email allowing you to reset your password.\
                    Please make sure to check your spam and trash if you can not find the email."
            )
            token =user.get_jwt()
            url = 'http://127.0.0.1:5000/password_reset/{}'.format(token)
            send_email(
                subject='WeChat - reset your password', 
                recipients=[user.email],
                text_body=url,
                html_body='<h1>{}</h1>'.format(url)
            )
        return redirect(url_for('login'))
    return render_template('password_reset_request.html', form=form)


def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_jwt(token)
    if not user:
        return redirect(url_for('login'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template(
        'password_reset.html',title='Password Reset',form=form
    )

@login_required
def explore():
    page_num = int(request.args.get('page') or 1)
    chats = Chat.query.order_by(Chat.create_time.desc()).paginate(
        page=page_num, per_page=current_app.config['CHAT_PER_PAGE'], error_out=False)

    next_url = url_for('index', page=chats.next_num) if chats.has_next else None
    prev_url = url_for('index', page=chats.prev_num) if chats.has_prev else None
    return render_template(
        'explore.html', chats=chats.items, next_url=next_url, prev_url=prev_url
    )

            
