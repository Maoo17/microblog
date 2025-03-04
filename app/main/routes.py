"""
Contains routes for main purpose of app
"""
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post
from app.main import bp


@bp.before_request
def before_request():
    """
    update last_seen for User before handling request
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_app.logger.debug("{} is authenticated".format(current_user))
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """
    Route for index page
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        current_app.logger.debug("{}".format(post))
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))

    posts = current_user.posts.all()
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts)


@bp.route('/explore')
@login_required
def explore():
    """
    Route for explore
    """
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts)


@bp.route('/user/<username>')
@login_required
def user(username):
    """
    Route for user
    """
    user_ = User.query.filter_by(username=username).first_or_404()
    posts = current_user.posts.all()
    return render_template('user.html', user=user_, posts=posts)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Route for editing user profile
    """
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():  # pylint: disable=no-else-return
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    """
    Route for following users
    """
    # pylint: disable=redefined-outer-name
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))
