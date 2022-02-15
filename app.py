import os
from urllib.parse import quote_plus
from requests import get
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask import Flask, jsonify, redirect, render_template, request, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)#creer une instance de l'application


app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:2356@localhost:5432/miniprojet_db"
#connexion a la base de données
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db=SQLAlchemy(app)#creer une instance de Dase de données
#migrate =Migrate(app,db)
#migrate = Migrate(app, db)


class Categorie(db.Model):
    __tablename__='categories'
    id=db.Column(db.Integer,primary_key=True)
    libelle_categorie=db.Column(db.String(100),nullable=False)

    def __init__(self,libelle_categorie) :
         self.libelle_categorie=libelle_categorie
    
    """def __init__(self,identity,libelle_categorie) :
         self.id=identity
         self.libelle_categorie=libelle_categorie"""
         
    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'libelle_categorie': self.libelle_categorie,
        }

db.create_all()
db.session.commit()
class Livre(db.Model):
    __tablename__='livres'
    id=db.Column(db.Integer, primary_key=True)
    isbn=db.Column(db.String(100),nullable=False)
    titre=db.Column(db.String(100),nullable=False)
    date_publication=db.Column(db.Date(),nullable=False)
    auteur=db.Column(db.String(100),nullable=False)
    editeur=db.Column(db.String(100),nullable=False)
    categorie_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)
    
    def __init__(self,isbn,titre,date_publication,auteur,editeur,categorie_id):
        self.isbn=isbn
        self.titre=titre
        self.date_publication=date_publication
        self.auteur=auteur
        self.editeur=editeur
        self.categorie_id=categorie_id

    """def __init__(self,id,isbn,titre,date_publication,auteur,editeur,categorie_id):
        self.isbn=isbn
        self.titre=titre
        self.date_publication=date_publication
        self.auteur=auteur
        self.editeur=editeur
        self.categorie_id=categorie_id
    """
    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'isbn':self.isbn,
        'titre':self.titre,
        'date_publication':self.date_publication,
        'auteur':self.auteur,
        'editeur':self.editeur,
        'categorie_id': self.categorie_id,
        }


db.create_all()
db.session.commit()
def verify_suppr_cat(id):
    liste=db.session.query(Livre.categorie_id).all()  
    return liste
###############################################################
#paginate function
###############################################################
def paginate(request):
    items = [item.format() for item in request]
    return items
###############################################################
#function to facilite the search of id,title or lib in our database
###############################################################
def cate_lib():
    liste=db.session.query(Categorie.libelle_categorie).all()
    liste="###".join([i[0] for i in liste])
    liste=liste.split("###")
    return liste
def cate_id():
    liste=db.session.query(Categorie.id).all()
    liste="###".join([str(i[0]) for i in liste])
    liste=[int(i) for i in liste.split("###")]
    return liste

def books_lib():
    liste=db.session.query(Livre.titre).all()
    liste="###".join([i[0] for i in liste])
    liste=liste.split("###")
    return liste

def books_id():
    liste=db.session.query(Livre.id).all()
    liste="###".join([str(i[0]) for i in liste])
    liste=[int(i) for i in liste.split("###")]
    return liste
###############################################################
#verify existance of id or title or lib functions
###############################################################
def exist_id_cat(id):
    if id in cate_id():
        return True
    return False
def exist_lib_cat(id):
    if id in cate_lib():
        return True
    return False
def exist_id_books(id):
    if id in books_id():
        return True
    return False
def exist_titre_books(id):
    if id in books_lib:
        return True
    return False  
###############################################################
#bad request function
###############################################################
def return_erk():
    return jsonify({
            'success': False,
            'error':400,
            'message': "unable to delete/patch category , category includes books ",
        })
def return_err():
    return jsonify({
            'success': False,
            'error':404,
            'message': "bad_request verify the existence of the object ",
        })
###############################################################
#CORS
###############################################################
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,POST,DELETE,OPTIONS')
    return response
###############################################################
#Main page
###############################################################
@app.route('/')
def init():
    return jsonify({
            'success': True,
            'code':200,
            'Lancement du piratage': "---------success-----------",
            'accés a  la machine':"*--------100%---------",
            'accés a la vie privé':"----------100%----------"
        })
###############################################################
#display all specific books by its title
###############################################################
@app.route('/livres/<string:word>')
def search_book(word):
    mot = '%'+word+'%'
    livre = Livre.query.filter(Livre.titre.like(mot)).all()
    livre = paginate(livre)
    return jsonify({
        'livre': livre
    })
###############################################################
#display all specific categorie by its libelle
###############################################################
@app.route('/categories/<string:word>')
def search_categorie(word):
    if exist_lib_cat(word):
        mot = '%'+word+'%'
        categorie = Categorie.query.filter(Categorie.libelle_categorie.like(mot)).all()
        categorie = paginate(categorie)
        return jsonify({
            'livre': categorie
        })
    else :
      return return_err()
###############################################################
#display all categories
###############################################################
@app.route('/categories')
def get_categories():
    categories = Categorie.query.all()
    categories = paginate(categories)
    return jsonify({
        'success': True,
        'Categorie': categories,
        'total_categories': len(categories)
    })
###############################################################
#display all books
###############################################################
@app.route('/livres')
def get_livres():
    livres= Livre.query.all()
    livres= paginate(livres)
    return jsonify({
        'success':True,
        'Livres':livres,
        'total_livres': len(livres)
    })
###############################################################
#display a specific category by its identifier(id)
###############################################################
@app.route('/categories/<int:id>')
def get_categorie(id):
    if exist_id_cat(id):
        categorie = Categorie.query.get(id)
        if categorie is None:
            abort(404)
        else:
            return categorie.format()
    else:
        return return_err()
###############################################################
#display a specific book by its identifier(id)
###############################################################
@app.route('/livres/<int:id>')
def get_livre(id):
    if exist_id_books(id):
        livre = Livre.query.get(id)
        if livre is None:
            abort(404)
        else:
            return livre.format()
    else:
        return return_err()
###############################################################
#delete a specific category by its identifier(id)
###############################################################
@app.route('/categories/<int:id>',methods=['DELETE'])
def delete_categorie(id):
    if exist_id_cat(id):
        categorie = Categorie.query.get(id)
        if len(verify_suppr_cat(id))==0:
            categorie.delete()
            return jsonify({
                'success': True,
                'delete successfully': id,
            })
        else:
            return return_erk()
        
    else:
        return return_err()
###############################################################
#delete a specific book by its identifier(id)
###############################################################
@app.route('/livres/<int:id>',methods=['DELETE'])
def delete_livres(id):
    if exist_id_books(id):
        livre =Livre.query.get(id)
        livre.delete()
        return jsonify({
            'success': True,
            'delete successfully': id,
        })
    else:
        return return_err()
###############################################################
#modify a specific category by its identifier(id)
###############################################################
@app.route('/categories/<int:id>',methods=['PATCH'] )
def update_categorie(id):
    if exist_id_cat(id):
        try:
            data = request.get_json()
            try:
              categorie= Categorie.query.get(id)
            except:
                abort(404)

            if len(data)!=0:
                if 'libelle_categorie' in data:
                    categorie.libelle_categorie = data['libelle_categorie']
                    #query.libelle_categorie = input()
                    categorie.update()
                else:
                    return jsonify({
                    'success': False,
                    'error':400,
                    'message': " bad request you have to enter empty fields",
                })
                return jsonify({
                    'success modify': True,
                    'categorie': categorie.format(),
                })
            else:
                return jsonify({
                    'success': False,
                    'error':400,
                    'message': " bad request you have to enter empty fields",
                })
        except:
            return jsonify({
                    'success': False,
                    'error':400,
                    'message': " bad request you have to enter empty fields",
                })
    else:
            return return_err()
###############################################################
#modify a specific book by its identifier(id)
###############################################################
@app.route('/livres/<int:id>',methods=['PATCH'] )
def update_livres(id):
    if exist_id_books(id):
        data = request.get_json()
        livre = Livre.query.get(id)
        try:
            if len(data)!=0:
                if   'titre' in data and 'auteur' in data and 'editeur' in data:
                    livre.titre = data['titre']
                    livre.auteur = data['auteur']
                    livre.editeur = data['editeur']
                else:
                    return jsonify({
                    'success': False,
                    'error':400,
                    'message': "You have entered empty information",
                    })
                livre.update()
            else:
                return jsonify({
                    'success': False,
                    'error':400,
                    'message': " bad request you have to enter empty fields",
                })
        except:
            return jsonify({
                'success': False,
                'error':400,
                'message': " bad request you have to enter empty fields",
            })
        return jsonify({
            'success modify': True,
            'livre': livre.format(),
        })
    else:
        return return_err()
###############################################################
#add a category
###############################################################
@app.route('/categories', methods=['POST'])
def add_categorie():
    data = request.get_json()
    idtf=libtf=False
    """if 'id' in data :
        idt=data['id']
        idtf=True"""
    if 'libelle_categorie' in data:
        libelle = data['libelle_categorie']
        libtf=True
    if libtf :
      categorie= Categorie(libelle)
    """else:
        categorie= Categorie(idt,libelle)"""
    categorie.insert()
    count = categorie.query.count()
    return jsonify({
        'success': True,
        'added': categorie.format(),
        'total_categorie': count,
    })
###############################################################
#add a book 
###############################################################
@app.route('/livres', methods=['POST'])
def add_livre():
    data = request.get_json()
    """if data['id']:
       id = data['id']"""
    isbn = data['isbn']
    titre = data['titre']
    date= data['date_publication']
    auteur = data['auteur']
    editeur = data['editeur']
    cateId = data['categorie_id']
    #if exist_id_books(id)==False  :
    livre= Livre(isbn,titre,date,auteur,editeur,cateId)
    """else:
        livre= Livre(isbn,titre,date,auteur,editeur,cateId)"""
    livre.insert()
    count = Livre.query.count()
    return jsonify({
        'success': True,
        'added': livre.format(),
        'total_livre': count,
    })
###############################################################
#view books in a category
###############################################################
@app.route('/categories/<int:id>/livres')
def get_livre_from_categorie(id):
    if exist_id_cat(id):
        books=db.session.query(Livre).join(Categorie).filter(Livre.categorie_id==id)
        books= paginate(books)
        return jsonify({
            'success':True,
            'Livres':books,
            'total_livres': len(books)
        }) 
    else:
        return return_err()   
