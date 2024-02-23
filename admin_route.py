from flask import render_template, request, url_for, redirect, flash, Blueprint
from flask_login import LoginManager, login_required, current_user
admin_page = Blueprint('admin_page', __name__, static_folder='static', template_folder='templates')


@admin_page.route("/category", methods=['GET', 'POST'])
@login_required
def category():
    from app import db
    
    if not is_admin():
        return 'access denied'
    # return 'its worked'
    from models.Category import Category
    from form_validator.categoryForm import CategoryFrom
    form = CategoryFrom(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully', 'success')
        return redirect(url_for('category'))
    categories = db.session.query(Category).all()
    return render_template('admin/category.html', categories=categories, title='category page', form=form)