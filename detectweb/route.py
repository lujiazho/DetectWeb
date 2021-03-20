from flask import render_template, redirect, url_for, request, \
    abort, current_app, flash
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import and_

from detectweb.forms import LoginForm, RegisterForm, EditProfileForm, TweetForm, \
    PasswdResetRequestForm, PasswdResetForm
from detectweb.models.user import User, load_user
from detectweb.models.tweet import Tweet
from detectweb.models.predict import Predict
from detectweb import db, utils
from detectweb.email_ import send_email
from detectweb.model import *

# 加上了login_required，页面就能被保护，需要先登录
@login_required
def index():
    # # 获取page参数，或者等于1，即默认就是显示第一页
    # page_num = int(request.args.get('page') or 1)
    # # index的tweet是自己+关注人的
    # tweets = current_user.own_and_followed_tweets().paginate(
    #     page=page_num, per_page=current_app.config['TWEET_PER_PAGE'], error_out=False)
    #
    # # tweets.next_num获取下一页的number，前提是还有下一页
    # next_url = url_for('index', page=tweets.next_num) if tweets.has_next else None
    # prev_url = url_for('index', page=tweets.prev_num) if tweets.has_prev else None
    # return render_template(
    #     'index.html', tweets=tweets.items, next_url=next_url, prev_url=prev_url
    # )
    return render_template('index.html')


def login():
    # session管理
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # 表示如果是点击submit触发的该函数
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None or not u.check_password(form.password.data):
            flash('非法用户名或密码', 'danger')
            return redirect(url_for('login'))
        # remember_me用于session管理，而不是记住用户名
        login_user(u, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if next_page: # 是否来自于跳转登录，如果是，那就返回到用户一开始点的那个页面去
            return redirect(next_page)
        return redirect(url_for('index')) # url_for通过函数名来找
    return render_template('login.html', title="Sign In", form=form)

def visitor():
    random_username = "visitor"+''.join(random.choice(string.digits) for _ in range(8))
    ip = request.remote_addr
    addr = utils.getAddrFromIP(ip)
    user = User(
        username=random_username,
        email=utils.RandomEmail(),
        country=addr["ct"],
        city=addr["city"],
        province=addr["prov"]
    )
    user.is_visitor = True
    # login_user(user)
    return render_template('index.html', current_user=user)

def logout():
    logout_user()
    return redirect(url_for('login'))


def register():
    # 如果是已登录状态，则直接返回index页面，不让注册
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # 获取ip
        ip = request.remote_addr
        print(ip)
        addr = utils.getAddrFromIP(ip)
        print(addr)
        # 创建表
        user = User(
            username=form.username.data,
            email=form.email.data,
            country=addr["ct"],
            city=addr["city"],
            province=addr["prov"]
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)

@login_required
def user(username):
    u = User.query.filter_by(username=username).first()
    if u is None: # 用户不存在，返回404
        abort(404)

    if request.method == 'POST':
        if request.form['request_button'] == 'Follow':
            current_user.follow(u)
            db.session.commit()
        elif request.form['request_button'] == "Unfollow":
            current_user.unfollow(u)
            db.session.commit()
        else:
            flash("邮件已发送, 请查看!", 'info')
            send_email_for_user_activate(current_user)
    return render_template('user.html', title='Profile', user=u)


# 生成url并发送邮件
def send_email_for_user_activate(user):

    token = user.get_jwt()
    url_user_activate = url_for(
        'user_activate',
        token=token,
        _external=True
    )
    send_email(
        subject=current_app.config['MAIN_SUBJECT_USER_ACTIVATE'],
        recipients=[user.email],
        text_body= render_template(
            'email/user_activate.txt',
            username=user.username,
            url_user_activate=url_user_activate
        ),
        html_body=render_template(
            'email/user_activate.html',
            username=user.username,
            url_user_activate=url_user_activate
        )
    )

# 点击链接后进入该函数激活
def user_activate(token):
    # # 这一句为作者误写，如果加了永远都激活不了
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    user = User.verify_jwt(token)
    if not user: # 如果没找到，其实不是expire了，因为没有判断是否expire，同一个链接永远都可以用，只能说明token是伪造的
        msg = "Token已过期d, 请尝试重新发送文件"
    else:
        user.is_activated = True
        db.session.commit()
        msg = '用户已激活!'
    return render_template(
        'user_activate.html', msg=msg
    )


def page_not_found(e):
    return render_template('404.html'), 404


@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'GET':
        form.about_me.data = current_user.about_me # 显示原来的
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data # 赋值
        db.session.commit() # 提交
        # 跳转
        return redirect(url_for('profile', username=current_user.username))
    return render_template('edit_profile.html', form=form)


def reset_password_request():
    # 如果已处于登录状态，就不需要重置密码了
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # 初始化这个form
    form = PasswdResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(
                "你将很快收到一封邮件，你能借此重置你的密码。 \
                 如果没有收到，请检查垃圾箱。", 'info'
            )
            # 用户请求的时候，服务器生成token
            token = user.get_jwt()
            # 生成reset密码的url
            url_password_reset = url_for(
                'password_reset',
                token=token,
                _external=True # 表示是完整的http链接：ip 端口 以及后面的url
            )
            url_password_reset_request = url_for(
                'reset_password_request',
                _external=True
            )
            send_email(
                subject=current_app.config['MAIL_SUBJECT_RESET_PASSWORD'], # 主题
                recipients=[user.email], # 接收者
                text_body= render_template(
                    'email/passwd_reset.txt',
                    url_password_reset=url_password_reset, # 传入url
                    url_password_reset_request=url_password_reset_request
                ),
                html_body=render_template(
                    'email/passwd_reset.html',
                    url_password_reset=url_password_reset,
                    url_password_reset_request=url_password_reset_request
                )
            )
            # 重置完了就返回登录页面
        return redirect(url_for('login'))
    return render_template('password_reset_request.html', form=form)


def password_reset(token):
    # 已经登录的情况下，同样不需要reset
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # 先验证，然后根据token返回一个user，然后对这个user的密码进行重置
    user = User.verify_jwt(token)
    if not user:
        # 重定向到login
        return redirect(url_for('login'))
    # 重置密码的form
    form = PasswdResetForm()
    # 提交后就覆盖之前的密码
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        # 重定向login
        return redirect(url_for('login'))
    return render_template(
        'password_reset.html', title='Password Reset', form=form
    )


@login_required
def explore():
    # get all user and sort by followers
    page_num = request.args.get('page') or "1"
    if page_num.isdigit():
        page_num = int(page_num)
    else:
        abort(404)
    tweets = Tweet.query.order_by(Tweet.create_time.desc()).paginate(
        page=page_num, per_page=current_app.config['TWEET_PER_PAGE'], error_out=False)

    next_url = url_for('explore', page=tweets.next_num) if tweets.has_next else None
    prev_url = url_for('explore', page=tweets.prev_num) if tweets.has_prev else None
    return render_template(
        'explore.html', tweets=tweets.items, next_url=next_url, prev_url=prev_url
    )

@login_required
def predict_history():
    u = User.query.filter_by(username=current_user.username).first()

    # 默认第一页
    page_num = request.args.get('page') or "1"
    if page_num.isdigit():
        page_num = int(page_num)
    else:
        abort(404)
    predicts = u.predicts.order_by(Predict.predict_time.desc()).paginate(
        page=page_num,
        per_page=current_app.config['PREDICT_PER_PAGE'],
        error_out=False)

    # 下一页的url
    next_url = url_for('predict_history', page=predicts.next_num, username=current_user.username) if predicts.has_next else None
    prev_url = url_for('predict_history', page=predicts.prev_num, username=current_user.username) if predicts.has_prev else None

    return render_template(
        'predict_history.html',
        title='History',
        allpredicts=predicts.items,
        user=u,
        next_url=next_url,
        prev_url=prev_url,
        totol_num=u.predicts.count() - (page_num-1)*current_app.config['PREDICT_PER_PAGE'],
        en2ch=utils.en2ch
    )

@login_required
def feedback_history():
    u = User.query.filter_by(username=current_user.username).first()

    # 默认第一页
    page_num = request.args.get('page') or "1"
    if page_num.isdigit():
        page_num = int(page_num)
    else:
        abort(404)
    feedbacks = u.tweets.order_by(Tweet.create_time.desc()).paginate(
        page=page_num,
        per_page=current_app.config['TWEET_PER_PAGE'],
        error_out=False)
    allfeedbacks = []
    for per in feedbacks.items:
        allfeedbacks.append("usr_predict_images/{}/{}.jpg".format(current_user.username, per.img))
    # 下一页的url
    next_url = url_for('feedback_history', page=feedbacks.next_num, username=current_user.username) if feedbacks.has_next else None
    prev_url = url_for('feedback_history', page=feedbacks.prev_num, username=current_user.username) if feedbacks.has_prev else None

    return render_template(
        'feedback_history.html',
        title='History',
        allfeedbacks=feedbacks.items,
        user=u,
        next_url=next_url,
        prev_url=prev_url,
        totol_num=u.tweets.count() - (page_num - 1) * current_app.config['TWEET_PER_PAGE']
    )

@login_required
def feedback():
    form = TweetForm()
    # 发文
    if form.validate_on_submit():
        t = Tweet(body=form.tweet.data, author=current_user, img=request.form['imgname'])
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('index'))
    u = User.query.filter_by(username=current_user.username).first()

    value = str(request.args.get('value') or None)

    designated = False
    if value == "None": # 没指定，则返回最新的图片
        # predict图片
        predict_img = u.predicts.order_by(Predict.predict_time.desc()).paginate(
            page=1,
            per_page=current_app.config['TWEET_PER_PAGE'],
            error_out=False)
        predict_img = predict_img.items[0]
        value = predict_img.img_name
    else: # value不为空表示指定了哪张图片
        predict_img = u.predicts.filter_by(img_name=value).first()
        designated = True

    find_ = u.tweets.filter_by(img=value).first()
    feedbacked = False
    if find_ is not None:
        feedbacked = True
    img_path = predict_img.img_path
    predict_img.img_path = "".join([img_path[:-33], '/', img_path[-32:]])
    return render_template('feedback.html',
                           form=form,
                           find_=find_,
                           feedbacked=feedbacked,
                           designated=designated,
                           predict_img=predict_img,
                           en2ch=utils.en2ch)

@login_required
def predict():
    if request.method == 'GET':
        return render_template('predict.html')
    if request.method == 'POST':
        message = request.get_json(force=True)
        encoded = message["image"]
        decoded = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(decoded))
        print(img.mode)
        now = datetime.datetime.now()

        destination = "static/usr_predict_images/{}".format(current_user.username)
        if not os.path.exists(destination):
            os.makedirs(destination)

        randomPost = False
        rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        if randomPost:
            ra1, ra2, ra3, ra4 = random.randint(15, 21), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
            randomtime_file = '20{}-0{}-1{}-1{}-33-48-'.format(ra1, ra2, ra3, ra4)
            randomtime_db = datetime.datetime.strptime('20{}-0{}-1{} 1{}:33:48'.format(ra1, ra2, ra3, ra4), "%Y-%m-%d %H:%M:%S")
            file_name = os.path.join(destination, randomtime_file + rand_str + '.jpg')
        else:
            file_name = os.path.join(destination, str(now.strftime("%Y-%m-%d-%H-%M-%S-")) + rand_str + '.jpg')


        try:
            if img.mode != "RGB": # jpeg是RGB
                img = img.convert('RGB')
            img.save(os.path.join(file_name), "JPEG", quality=80, optimize=True, progressive=True)
        except IOError:
            ImageFile.MAXBLOCK = img.size[0] * img.size[1]
            img.save(file_name, "JPEG", quality=80, optimize=True, progressive=True)

        t = label_image.read_tensor_from_image_file(file_name,
                                                    input_height=input_height,
                                                    input_width=input_width,
                                                    input_mean=input_mean,
                                                    input_std=input_std)

        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        input_operation = graph.get_operation_by_name(input_name);
        output_operation = graph.get_operation_by_name(output_name);

        with tf.Session(graph=graph) as sess:
            start = time.time()
            results = sess.run(output_operation.outputs[0],
                               {input_operation.outputs[0]: t})
            end = time.time()

        results = np.squeeze(results)

        top_k = results.argsort()[-5:][::-1]
        labels = label_image.load_labels(label_file)

        print('\nEvaluation time (1-image): {:.3f}s\n'.format(end - start))

        # top_k [35 18 29 28 30]
        for i in top_k:
            if max(results) == results[i]:
                res = results[i]
                lab = labels[i]
                print(labels[i], results[i], "this is max")
            else:
                print(labels[i], results[i], "this is not max")
        # 入库
        if randomPost:
            t = Predict(img_name=file_name[-32:-4], img_path=file_name, size=str(img.size[0]) + "*" + str(img.size[1]),
                        predict_time=randomtime_db, predict_result=lab, predict_value=str(res), author=current_user)
        else:
            t = Predict(img_name=file_name[-32:-4], img_path=file_name, size=str(img.size[0]) + "*" + str(img.size[1]),
                        predict_result=lab, predict_value=str(res), author=current_user)
        ch = utils.en2ch[lab]
        db.session.add(t)
        db.session.commit()
        response = {
            'prediction': {
                'species': ch.split(' ')[0],
                'condition': ' '.join(ch.split(' ')[1:]),
                'value': str(res)
            }
        }
        return jsonify(response)

@login_required
def predictbykind():
    if request.method == 'POST':
        value = request.get_json(force=True)["value"]
        encoded = request.get_json(force=True)["image"]
        decoded = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(decoded))

        # 保存图片
        now = datetime.datetime.now()
        destination = "static/usr_predict_images/{}".format(current_user.username)
        if not os.path.exists(destination):
            os.makedirs(destination)
        rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        file_name = os.path.join(destination, str(now.strftime("%Y-%m-%d-%H-%M-%S-")) + rand_str + '.jpg')
        try:
            if image.mode != "RGB": # jpeg是RGB
                image = image.convert('RGB')
            image.save(os.path.join(file_name), "JPEG", quality=80, optimize=True, progressive=True)
        except IOError:
            ImageFile.MAXBLOCK = image.size[0] * image.size[1]
            image.save(file_name, "JPEG", quality=80, optimize=True, progressive=True)

        response = utils.infer_special(value, image)

        # 入库
        t = Predict(img_name=file_name[-32:-4], img_path=file_name, size=str(image.size[0]) + "*" + str(image.size[1]),
                    predict_result=" ".join([value, response['conditionen']]),
                    predict_value=response['prediction']['value'], author=current_user)
        db.session.add(t)
        db.session.commit()
    return jsonify(response)

@login_required
def dashboard():
    time_now = datetime.datetime.now()

    # join实现复杂查询https://www.kancloud.cn/tokimeki/flask_notebook/775173
    # 方法一，查看有病的
    same_city_count = 0
    for u, a in db.session.query(User, Predict).filter(User.id == Predict.user_id).all():
        if u.city == current_user.city and 'healthy' not in a.predict_result:
            same_city_count+=1

    # 方法二，查看有病的，只要包含healthy的label就不算有病
    all_of_same_city = Predict.query.join(User, (User.id == Predict.user_id)).filter_by(city=current_user.city).filter(and_(Predict.predict_result.notlike('%healthy%'), Predict.predict_result.notlike('%healthy')))

    # 以后按这样来，以免算法有问题，如果两个都一致，结果就没问题
    assert same_city_count == all_of_same_city.count()

    timeline = request.args.get('timeline') or "week"
    type_ = request.args.get('type') or "allkinds"

    return utils.getStatistics(timeline, type_, all_of_same_city, time_now, current_user)


def predict_for_visitor():
    if request.method == 'GET':
        try:
            username = request.args.get('username')
        except:
            print("重造")
            username = "visitor" + ''.join(random.choice(string.digits) for _ in range(8))
        ip = request.remote_addr
        addr = utils.getAddrFromIP(ip)
        user = User(
            username=username,
            email=utils.RandomEmail(),
            country=addr["ct"],
            city=addr["city"],
            province=addr["prov"]
        )
        user.is_visitor = True
        return render_template('predict.html', current_user=user)
    if request.method == 'POST':
        value = request.get_json(force=True)["value"]
        encoded = request.get_json(force=True)["image"]
        decoded = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(decoded))
        if image.mode != "RGB":  # jpeg是RGB
            image = image.convert('RGB')
        response = utils.infer_special(value, image)
    return jsonify(response)


def intro():
    value = str(request.args.get('value') or "apple")
    if value in utils.classname:
        return render_template("intros/intro_{}.html".format(value))
    abort(404)


def article():
    value = request.args.get('value') or "1"
    if value.isdigit():
        value = int(value)
    else:
        abort(404)
    if value == 1:
        return render_template("articles/article{}.html".format(value))
    if value == 2:
        return render_template("articles/article{}.html".format(value))
    abort(404)