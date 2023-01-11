from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from website.models import Ideas
from website import db
import openai
import os

views = Blueprint('views', __name__)

openai.api_key = os.environ["OPENAI_API_KEY"]
prompt_txt = "em poucas palavras, sugira uma ideia de startup com base no tema "
temas = ["erradicação da pobreza", "agricultura sustentável", "educação de qualidade", "água potável",
"saneamento básico", "energia limpa", "energia acessível", "equidade de gênero", "empregabilidade", "inovação social",
"redução das desigualdades", "comunidades sustentáveis", "consumo consciente", "produção responsável", "mudança global do clima",
"vida na água", "paz  e justiça", "instituições eficazes", "vida terrestre", "promover o desenvolvimento e a transferência de tecnologia"]
temas = temas + temas

@views.route('/', methods=['GET', 'POST'])
def home():
    if Ideas.query.all() == []:
        for tema in temas:
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_txt + tema,
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
            if idea.like_counter >= 3:
                if any(x.generated_by == idea.id for x in generated_ideas):
                    pass
                else:
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="sugira uma breve ideia de startup com base na ideia: " + idea.text,
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