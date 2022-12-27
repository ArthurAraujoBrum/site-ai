from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from website.models import Ideas
from website import db
import openai

views = Blueprint('views', __name__)

openai.api_key = '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'
prompt = "sugira uma breve ideia de startup que gere impacto social:"

@views.route('/', methods=['GET', 'POST'])
def home():
    if Ideas.query.all() == []:
        for i in range(10):
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1,
            )
            idea = Ideas(text=response["choices"][0]["text"].strip(), generated_by=0, like_counter=0)
            db.session.add(idea)
            db.session.commit()
        return redirect(url_for('views.home'))
    else:
        ideas = Ideas.query.order_by(Ideas.like_counter.desc())
        generated_ideas = Ideas.query.filter_by(generated=True).all()
        for idea in ideas:
            if idea.like_counter > 5:
                if any(x.generated_by == idea.id for x in generated_ideas):
                    pass
                else:
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="sugira uma breve ideia de startup que gere impacto social com base na ideia: " + idea.text,
                    temperature=0.6,
                    max_tokens=150,
                    top_p=1,
                    frequency_penalty=1,
                    presence_penalty=1,
                    )
                    new_idea = Ideas(text=response["choices"][0]["text"].strip(), generated_by=idea.id, generated=True, like_counter=0)
                    db.session.add(new_idea)
                    db.session.commit()
    original_ideas = Ideas.query.filter_by(generated=False).order_by(Ideas.like_counter.desc())
    return render_template("home.html", cards=original_ideas, new_cards=generated_ideas)

@views.route('/init-database')
def init_database():
    for i in range(10):
        idea = Ideas(text='Teste número '+str(i), generated_by=0, like_counter=0)
        db.session.add(idea)
        db.session.commit()
    flash('Database Created!', category='success')
    return redirect(url_for('views.home'))

@views.route('/like-idea/<idea_id>', methods=['POST'])
def like_idea(idea_id):
    idea = Ideas.query.filter_by(id=idea_id).first()
    idea.like_counter = idea.like_counter + 1
    db.session.commit()
    #return redirect(url_for('views.home'))
    return jsonify({"likes": idea.like_counter})

@views.route('/dislike-idea/<idea_id>', methods=['POST'])
def dislike_idea(idea_id):
    idea = Ideas.query.filter_by(id=idea_id).first()
    idea.like_counter = idea.like_counter - 1
    db.session.commit()
    #return redirect(url_for('views.home'))
    return jsonify({"likes": idea.like_counter})