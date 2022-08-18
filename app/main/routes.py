from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EmptyForm, AddClientForm, EditClientForm
from app.models import Therapist,Client
from app.main import bp




@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    clients = current_user.user_clients()
    title = f"{current_user.first_name},{current_user.last_name} בתי אב "

    return render_template('index.html', title=title,clients=clients)



@bp.route('/client/<client_id>')
@login_required
def client(client_id):
    client = Client.query.filter_by(id=client_id).first_or_404()
    therapist_uname = Therapist.query.filter_by(id=client.therapist_id).first().username
    return render_template('client.html', client=client,therapist_uname=therapist_uname)

@bp.route('/client/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    thera_id = []
    thera = Therapist.query.all()
    for t in thera:
        thera_id.append(t.username)
    form = AddClientForm()
    form.therapist_id.choices = thera_id

    th = Therapist.query.filter_by(username=form.therapist_id.data).first()

    if form.validate_on_submit():
        client = Client(
            main_first_name=form.main_first_name.data,
            main_last_name=form.main_last_name.data,
            main_id=form.main_id.data,
            main_birth_year=form.main_birth_year.data,
            main_phone=form.main_phone.data,
            main_is_dutch=form.main_is_dutch.data,
            main_is_davids=form.main_is_davids.data,
            main_status=form.main_status.data,

            second_first_name=form.second_first_name.data,
            second_last_name=form.second_last_name.data,
            second_id=form.second_id.data,
            second_birth_year=form.second_birth_year.data,
            second_phone=form.second_phone.data,
            second_is_dutch=form.second_is_dutch.data,
            second_status=form.second_status.data,
    
            address_city=form.city_choice.data,
            address_street=form.street_choice.data,
            address_house_num=form.address_house_num.data,
            therapist_id=th.id,
            description=form.description.data,
                        )
        db.session.add(client)
        db.session.commit()

        flash('Congratulations, you add a new Client!')
        return redirect(url_for('main.add_client'))
    return render_template('add_client.html', title='הוסף לקוח',
                           form=form)


@bp.route('/client/edit_client/<client_id>', methods=['GET', 'POST'])
@login_required
def edit_client():
    form = EditClientForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_client.html', title='ערוך פרופיל לקוח',
                           form=form)

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = Therapist.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)


# @bp.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm(current_user.username)
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.about_me = form.about_me.data
#         db.session.commit()
#         flash(_('Your changes have been saved.'))
#         return redirect(url_for('main.edit_profile'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.about_me.data = current_user.about_me
#     return render_template('edit_profile.html', title=_('Edit Profile'),
#                            form=form)


# @bp.route('/follow/<username>', methods=['POST'])
# @login_required
# def follow(username):
#     form = EmptyForm()
#     if form.validate_on_submit():
#         user = Therapist.query.filter_by(username=username).first()
#         if user is None:
#             flash('User %(username)s not found.', username=username)
#             return redirect(url_for('main.index'))
#         if user == current_user:
#             flash('You cannot follow yourself!')
#             return redirect(url_for('main.user', username=username))
#         current_user.follow(user)
#         db.session.commit()
#         flash(_('You are following %(username)s!', username=username))
#         return redirect(url_for('main.user', username=username))
#     else:
#         return redirect(url_for('main.index'))
#
#
# @bp.route('/unfollow/<username>', methods=['POST'])
# @login_required
# def unfollow(username):
#     form = EmptyForm()
#     if form.validate_on_submit():
#         user = Therapist.query.filter_by(username=username).first()
#         if user is None:
#             flash(_('User %(username)s not found.', username=username))
#             return redirect(url_for('main.index'))
#         if user == current_user:
#             flash(_('You cannot unfollow yourself!'))
#             return redirect(url_for('main.user', username=username))
#         current_user.unfollow(user)
#         db.session.commit()
#         flash(_('You are not following %(username)s.', username=username))
#         return redirect(url_for('main.user', username=username))
#     else:
#         return redirect(url_for('main.index'))
#
#
#
#
#
# @bp.route('/search')
# @login_required
# def search():
#     if not g.search_form.validate():
#         return redirect(url_for('main.explore'))
#     page = request.args.get('page', 1, type=int)
#     posts, total = Therapist.search(g.search_form.q.data, page,
#                                current_app.config['POSTS_PER_PAGE'])
#     next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
#         if total > page * current_app.config['POSTS_PER_PAGE'] else None
#     prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
#         if page > 1 else None
#     return render_template('search.html', title=_('Search'), posts=posts,
#                            next_url=next_url, prev_url=prev_url)
#

# @bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
# @login_required
# def send_message(recipient):
#     user = User.query.filter_by(username=recipient).first_or_404()
#     form = MessageForm()
#     if form.validate_on_submit():
#         msg = Message(author=current_user, recipient=user,
#                       body=form.message.data)
#         db.session.add(msg)
#         user.add_notification('unread_message_count', user.new_messages())
#         db.session.commit()
#         flash(_('Your message has been sent.'))
#         return redirect(url_for('main.user', username=recipient))
#     return render_template('send_message.html', title=_('Send Message'),
#                            form=form, recipient=recipient)


# @bp.route('/messages')
# @login_required
# def messages():
#     current_user.last_message_read_time = datetime.utcnow()
#     current_user.add_notification('unread_message_count', 0)
#     db.session.commit()
#     page = request.args.get('page', 1, type=int)
#     messages = current_user.messages_received.order_by(
#         Message.timestamp.desc()).paginate(
#             page, current_app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('main.messages', page=messages.next_num) \
#         if messages.has_next else None
#     prev_url = url_for('main.messages', page=messages.prev_num) \
#         if messages.has_prev else None
#     return render_template('messages.html', messages=messages.items,
#                            next_url=next_url, prev_url=prev_url)


# @bp.route('/export_posts')
# @login_required
# def export_posts():
#     if current_user.get_task_in_progress('export_posts'):
#         flash(_('An export task is currently in progress'))
#     else:
#         current_user.launch_task('export_posts', _('Exporting posts...'))
#         db.session.commit()
#     return redirect(url_for('main.user', username=current_user.username))


# @bp.route('/notifications')
# @login_required
# def notifications():
#     since = request.args.get('since', 0.0, type=float)
#     notifications = current_user.notifications.filter(
#         Notification.timestamp > since).order_by(Notification.timestamp.asc())
#     return jsonify([{
#         'name': n.name,
#         'data': n.get_data(),
#         'timestamp': n.timestamp
#     } for n in notifications])
