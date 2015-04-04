from flask import Flask, jsonify, redirect, url_for, escape, abort, request, render_template
from syzoj import oj
from syzoj.models import User, Problem, get_problem_by_id, File, JudgeState, WaitingJudge, get_user, Article
from syzoj.views.common import need_login, not_have_permission, show_error, pretty_time, Paginate
from urllib import urlencode


@oj.route("/discussion")
def discussion():
    query = Article.query

    def make_url(page, other):
        return url_for("discussion") + "?" + urlencode({"page": page})

    sorter = Paginate(query, make_url=make_url, cur_page=request.args.get("page"), edge_display_num=3, per_page=10)
    return render_template("discussion.html", user=get_user(), articles=sorter.get(), pretty_time=pretty_time,
                           tab="discussion", sorter=sorter)


@oj.route("/article/<int:article_id>")
def article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if not article:
        return show_error("Can't find article", url_for('index'))
    print article.title
    return render_template("article.html", article=article, user=get_user(), pretty_time=pretty_time, tab="discussion")


@oj.route("/article/<int:article_id>/edit", methods=["GET", "POST"])
def edit_article(article_id):
    user = get_user()
    if not user:
        return need_login()

    article = Article.query.filter_by(id=article_id).first()
    if article and article.is_allowed_edit(user) == False:
        return not_have_permission()

    if request.method == "POST":
        if request.form.get("title") == "" or request.form.get("content") == "":
            return show_error("Please input title and content",
                              url_for("edit_article", article_id=article_id))
        if not article:
            article = Article(title=request.form.get("title"), content=request.form.get("content"), user=user)

        article.title = request.form.get("title")
        article.content = request.form.get("content")
        article.save()
        return redirect(url_for("article", article_id=article.id))
    else:
        return render_template("edit_article.html", user=get_user(), article=article, tab="discussion")


@oj.route("/article/<int:article_id>/delete")
def delete_article(article_id):
    user = get_user()
    article = Article.query.filter_by(id=article_id).first()

    if not user:
        return need_login()

    if not article:
        return show_error("Can't find article", url_for('index'))

    if article and article.is_allowed_edit(user) == False:
        return not_have_permission()

    if request.args.get("confirm")=="true":
        article = Article.query.filter_by(id=article_id).first()
        if article and article.is_allowed_edit(user) == False:
            return not_have_permission()

        article.delete()
        return redirect(url_for("discussion"))
    else:
        return render_template("delete_article.html",user=user,article=article)