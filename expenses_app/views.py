from flask import current_app as app, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from expenses_app.forms import CreateGroup, AddUserToGroup, RemoveUserFromGroup, AddAccountToGroup, RemoveAccountFromGroup
from expenses_app.models import db, User, Group, Account


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = CreateGroup()
    if form.validate_on_submit():
        new_group_name = form.name.data
        exists = Group.query.filter(Group.name == new_group_name).first()
        if not exists:
            current_user.create_group(new_group_name)
            db.session.commit()
        else:
            flash(f"{new_group_name} has already been taken! Try another name.")
    return render_template("index.html", form=form)


@app.route("/groups/<group_name>/summary", methods=["GET", "POST"])
@login_required
def group_summary(group_name):
    group = group_from_group_name(group_name)

    if group and group.has_user(current_user):
        return render_template("group_summary.html", group=group)

    return redirect(url_for("index"))


@app.route("/groups/<group_name>/access", methods=["GET", "POST"])
@login_required
def group_access(group_name):
    group = group_from_group_name(group_name)
    if group and group.has_user(current_user):
        add_form = AddUserToGroup()
        remove_form = RemoveUserFromGroup.from_group(group, current_user)

        return render_template("group_access.html", group=group, add_form=add_form, remove_form=remove_form)

    return render_template("index.html", group=group)


@app.route("/groups/<group_name>/remove_user", methods=["POST"])
@login_required
def remove_user_from_group(group_name):
    group = group_from_group_name(group_name)
    remove_form = RemoveUserFromGroup.from_group(group, current_user)
    if remove_form.validate_on_submit():
        user_id = remove_form.username.data
        old_user = User.query.get(user_id)
        group.remove_user(old_user)
        db.session.commit()
    return redirect(url_for("group_access", group_name=group_name))


@app.route("/groups/<group_name>/add_user", methods=["POST"])
@login_required
def add_user_to_group(group_name):
    group = group_from_group_name(group_name)
    add_form = AddUserToGroup()
    if add_form.validate_on_submit():
        user_name = add_form.username.data
        new_user = User.query.filter_by(username=user_name).first()
        if new_user:
            group.add_user(new_user)
            db.session.commit()
        else:
            flash(f"{user_name} is not a valid username!")
    return redirect(url_for("group_access", group_name=group_name))


@app.route("/groups/<group_name>/accounts")
@login_required
def group_accounts(group_name):
    group = group_from_group_name(group_name)

    if group and group.has_user(current_user):
        add_form = AddAccountToGroup.from_group(group)
        remove_form = RemoveAccountFromGroup.from_group(group)
        return render_template("group_accounts.html", group=group, add_form=add_form, remove_form=remove_form)

    return redirect(url_for(index))


@app.route("/groups/<group_name>/add_account", methods=["POST"])
@login_required
def add_account_to_group(group_name):
    group = group_from_group_name(group_name)
    add_form = AddAccountToGroup.from_group(group)
    if add_form.validate_on_submit():
        name = add_form.name.data
        name_exists = Account.query.filter(Account.name == name, Account.group_id == group.id).first()
        if name_exists:
            flash("The account name already exists in this group!")
        else:
            user_id = add_form.user.data
            user = User.query.get(user_id) if user_id > -1 else None
            has_balance = add_form.has_balance.data
            balance = add_form.starting_balance.data if has_balance else None
            Account.create_account(group, name, user, balance)
            db.session.commit()

    return redirect(url_for("group_accounts", group_name=group_name))


@app.route("/groups/<group_name>/remove_account", methods=["POST"])
@login_required
def remove_account_from_group(group_name):
    group = group_from_group_name(group_name)
    remove_form = RemoveAccountFromGroup.from_group(group)
    if remove_form.validate_on_submit():
        account_id = remove_form.name.data
        old_account = Account.query.get(account_id)
        group.remove_account(old_account)
        old_account.status = "removed"
        db.session.commit()

    return redirect(url_for("group_accounts", group_name=group_name))


def group_from_group_name(group_name):
    return Group.query.filter(Group.name == group_name).first()
