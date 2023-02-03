from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from website.models import Ideas
from website import db
import openai
import os

views = Blueprint('views', __name__)

openai.api_key = os.environ["OPENAI_API_KEY"]
prompt_txt = "em uma frase curta, sugira uma startup envolvendo "
categorias = ["Direitos Humanos", "Equidade", "Erradicação da pobreza", "Inovação", "Sustentabilidade"]
categorias_list = categorias + categorias
dic_categorias = {"Direitos Humanos":["educação de qualidade", "água potável", "saneamento básico", "paz e justiça"], "Equidade":["equidade de gênero", "inclusão social", "redução das desigualdades sociais"], "Erradicação da pobreza":["erradicação da pobreza", "empregabilidade"], "Inovação":["inovação social", "instituições eficazes", "promover o desenvolvimento e a transferência de tecnologia"], "Sustentabilidade":["energia limpa", "energia acessível", "comunidades sustentáveis", "consumo consciente", "produção responsável", "mudança global do clima", "vida na água", "vida terrestre"]}
@views.route('/', methods=['GET', 'POST'])
def home():
    if Ideas.query.all() == []:
        for cat in categorias_list:
            for tema in dic_categorias[cat]:
                response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt_txt + tema,
                temperature=0.6,
                max_tokens=150,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1,
                )
                idea = Ideas(text=response["choices"][0]["text"].strip(), generated_by=0, generation=0, category=cat, like_counter=0)
                db.session.add(idea)
                db.session.commit()
        return redirect(url_for('views.home'))
    else:
        ideas = Ideas.query.order_by(Ideas.like_counter.desc())
        generated_ideas = Ideas.query.filter(Ideas.generation>0).all()
        for idea in ideas:
            if idea.like_counter >= 3:
                if ((idea.like_counter/3).is_integer()==True and len(Ideas.query.filter(Ideas.generation>0).filter(Ideas.generated_by==idea.id).all())<int(idea.like_counter/3)):
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="em até duas frases, sugira uma startup com base na ideia: " + idea.text,
                    temperature=0.6,
                    max_tokens=150,
                    top_p=1,
                    frequency_penalty=1,
                    presence_penalty=1,
                    )
                    new_idea = Ideas(text=response["choices"][0]["text"].strip(), generated_by=idea.id, generation=idea.generation+1, category=idea.category, like_counter=0)
                    db.session.add(new_idea)
                    db.session.commit()
                else:
                    pass
    ideas_dict = {}
    for cat in categorias:
        ideas_dict[cat] = Ideas.query.filter_by(category=cat).order_by(Ideas.like_counter.desc())
    return render_template("home.html", sections=categorias, cards=ideas_dict)

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