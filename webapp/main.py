from . import db
from flask import Blueprint, render_template,url_for,redirect,request,session
from flask_login import  login_required
from .dbmodels import Boeken,Lenen,Users,Leerlingen
from sqlalchemy import insert,join
import datetime


main = Blueprint('main',__name__)


#Functions
#Functie new_leen krijgt de leering mee als waarde en zal dan de nieuwe 'leen' aanmaken en deze linken op de nodige plaatsen in de database
def new_leen(leerling):
    boekid = session.get("boekid",None)
    boek = Boeken.query.filter_by(BoekID=boekid).first()
    user = Users.query.filter_by(id=1).first()
    new_leen = Lenen(datum=datetime.datetime.now(),userID=user.id,BoekID=boek.BoekID,LeerlingID=leerling.LeerlingID)
    db.session.add(new_leen)
    db.session.commit()
    leen = Lenen.query.order_by((Lenen.datum).desc()).first()
    boek.LeenID = leen.LeenID 
    db.session.commit()
    succes = "Het boek werd uitgeleend"
    return succes


#deze functie gaat na kijken of een leerling al niet in bezit is van een boek
def check_lln_boek(curlln):
    boek_lln = Leerlingen.query.join(Lenen).filter(Lenen.LeerlingID==curlln.LeerlingID).first()
    if(boek_lln == None):
        return True
    else:
        return False


#funcite gaat alle info die met de 'leen' te maken heeft verwijderen zo dat een boek weer vrij is.
def inleveren_boek(boekid):
    boek = Boeken.query.filter_by(BoekID=boekid).first()
    boek.LeenID = None
    Lenen.query.filter_by(BoekID=boek.BoekID).delete()
    db.session.commit()
    succes = "Het boek werd succesvol ingeleverd"
    return succes

#functie gaat stap voor stap de collommen doorlope, telkens wanneer er geen resultaat is wordt er naar de volgende gegeaan.
def opzoeken(zoekterm):
    gevonden_boeken = []
    if(zoekterm):
        if(gevonden_boeken == []):
            gevonden_boeken = Boeken.query.filter_by(BoekID=zoekterm).all()
            print(gevonden_boeken)                 
        if(gevonden_boeken == []):
            gevonden_boeken = Boeken.query.filter(Boeken.auteur.like('%'+zoekterm+'%')).all()
            print(gevonden_boeken,2)
        if(gevonden_boeken == []):
            gevonden_boeken = Boeken.query.filter(Boeken.titel.like('%'+zoekterm+'%')).all()
        if(gevonden_boeken == []):
            gevonden_boeken = Boeken.query.filter(Boeken.afkorting_auteur.like('%'+zoekterm+'%')).all()
        if(gevonden_boeken == []):
           gevonden_boeken = Boeken.query.filter(Boeken.isbn.like('%'+zoekterm+'%')).all()
        if(gevonden_boeken == []):
            gevonden_boeken = Boeken.query.filter(Boeken.categorie.like('%'+zoekterm+'%')).all()
        if(gevonden_boeken == []):
           gevonden_boeken = Boeken.query.filter(Boeken.nummer_jaartal_volgnummer.like('%'+zoekterm+'%')).all()
        return gevonden_boeken

#main pagina
@main.route('/index', methods = ["POST","GET"])
@login_required
def index():
    return render_template("index.html")


#Op deze pagina is het mogelijk ze zoeken naar specifieke boeken
@main.route('/boeken', methods = ["POST","GET"])
#@login_required
def boeken():
    error = None
    gevonden_boeken = []
    disp_table = False
    status_boek = False #false = =niet uitgeleend, true = uitegeleend 
    if(request.method == 'POST'):
        zoekterm = request.form['opzoeking']
        print(zoekterm)
        gevonden_boeken = opzoeken(zoekterm)
        if(gevonden_boeken != []):
            disp_table = True
        else:
            error = 'Er werden geen boeken gevonden.'

    return render_template("boeken.html",gevonden_boeken=gevonden_boeken,disp_table=disp_table,error=error)

#lenen van boeken
@main.route('/lenen', methods = ["POST","GET"])
@login_required
def lenen():
    boek = None
    error = None
    disp_zoekbalk = True
    llnform = False
    if(request.method == 'POST'):
        boekid = request.form['boekid']
        boek = Boeken.query.filter_by(BoekID=boekid).first()
        user = Users.query.filter_by(id=1).first()
        session["boekid"] = boekid
        if(boek): #nakijken of er een boek gevonden is 
            if(boek.LeenID == None):
                llnform= True
                disp_zoekbalk = False
            else:
                error = 'Dit boek is reeds uitgeleend'
                disp_zoekbalk = False
        else:
            error = 'Er werd geen boek gevonden met dit ID'
    return render_template('lenen.html',disp_zoekbalk=disp_zoekbalk,llnform=llnform,boek=boek,error=error)

#pagina heeft zelfde template als '/lenen', op deze pagina wordt de leerling zijn data na gekeken. 
#Moet enkel aangemaakt worden wanneer er een boek effectief ontleent wordt.
@main.route('/ontlenen',methods = ['POST','GET'])
@login_required
def ontlenen():
    llnform = False
    succes = None
    error = None
    boek = None
    disp_boek = None
    if(request.method == 'POST'):
        disp_boek = False
        llnform = False
        boek = session.get("boek",None)
        session.pop

        voornaam = request.form['Voornaam']
        naam = request.form['Naam']
        klas = request.form['Klas']
        klas_nr = request.form['KlasNr']
        if(voornaam == "" or naam == "" or klas == "" or klas_nr == ""):
            error = "Gelieve alle velden in te vullen."
        elif (len(voornaam)> 100):
            error = "Voornaam van de leerling is te lang voor de database."
        elif(len(naam)>100):
            error = "De naam van de leerling is te lang voor de database."
        elif(len(klas)>10):
            error = "De klas van de leerling is te lang voor de database."
        elif(len(klas_nr)>2):
            error = "Het klas nummer is niet geldig (max 2 cijfers)."
        else:
            curLln = Leerlingen.query.filter_by(voornaam=voornaam,naam=naam,klas=klas,klas_nr=klas_nr).first()
            if(curLln):
                if(check_lln_boek(curLln)):
                    succes = new_leen(curLln)
                else:
                    error = "De leerling heeft reeds een boek in zijn bezit."

            else:
                #Toevoegen nieuwe leerling
                new_lln = Leerlingen(voornaam=voornaam,naam=naam,klas=klas,klas_nr=klas_nr)
                db.session.add(new_lln)
                db.session.commit()
                curLln = Leerlingen.query.filter_by(voornaam=voornaam,naam=naam,klas=klas,klas_nr=klas_nr).first()
                succes = new_leen(curLln)
    return render_template('lenen.html',boek=boek,llnform=llnform,disp_boek=disp_boek,succes=succes,error=error)

#het terug brengen van boeken
@main.route('/inleveren', methods = ["POST","GET"])
@login_required
def inleveren():
    error = None
    disp_zoekbalk = True
    disp_form = False
    boek = None
    if(request.method == 'POST'):
        boekid = request.form['boekid']
        boek = Boeken.query.filter_by(BoekID=boekid).first()
        if(boek):
            if(boek.LeenID != None): #bij 'none' staat er geen waarde in de tabel, is het boek dus ook niet uitgeleend
                disp_zoekbalk = False
                session["boekid"] = boek.BoekID
                disp_form = True                
            else:
                error = 'Het boek dat u wilt inleveren is niet uitgeleend'             
                #return render_template("inleveren.html",disp_zoekbalk=disp_zoekbalk,error=error,boek=boek)
        else:
            error = 'Er werd geen boek gevonden met dit ID'
            #return render_template("inleveren.html",disp_zoekbalk=disp_zoekbalk,error=error,boek=boek)

    return render_template("inleveren.html",disp_zoekbalk=disp_zoekbalk,error=error,disp_form=disp_form,boek=boek)

@main.route('/inleveren_defnitief',methods= ["POST","GET"])
@login_required
def inleveren_defnitief():
    disp_zoekbalk = False
    disp_form = True 
    error = None
    boekid = session.get("boekid",None)
    session.pop
    boek = Boeken.query.filter_by(BoekID=boekid)
    if(request.method == 'POST'):
        confirm = request.form['confirm']
        if(confirm == "True"):
            disp_zoekbalk = False
            disp_form = False
            succes = inleveren_boek(boekid)
        elif(confirm == "False"):
            return redirect(url_for('main.inleveren'))

    return render_template('inleveren.html',disp_zoekbalk=disp_zoekbalk,error=error,disp_form=disp_form,succes=succes)



#pagina zorgt er voor dat er nieuwe boeken kunnen worden toegevoegd aan de database
@main.route('/beheer', methods = ["POST","GET"])
@login_required
def beheer():
    error = None
    succes = None
    if(request.method == 'POST'):
        titel_boek = request.form['Titel_boek']
        naam_auteur = request.form['Naam_auteur']
        afkorting_auteur = request.form['Afkorting_auteur']
        isbn = request.form['ISBN_nummer']
        nr_bib = request.form['Nummer_bib']
        categorie = request.form.getlist('categorie')
        #print(titel_boek,naam_auteur,afkorting_auteur,isbn,nr_bib,categorie)
        if (len(titel_boek)> 150):
            error = "Titel van het boek is te lang voor de database."
        elif(len(naam_auteur)> 50):
            error = "Naam van de Auteur is te lang voor de database."
        elif(len(afkorting_auteur)>5):
            error = "De afkorting van de auteur mag max 5 karakters bevatten."
        elif(len(isbn)>30):
            error = "ISBN nummer is te lang voor de database."
        elif(len(nr_bib)>15):
            error = "Nummer bib is te lang voor de database."
        elif(categorie == ""):
            error = "Er is geen categorie gekozen!"
        elif(titel_boek == "" and naam_auteur == "" and afkorting_auteur == "" and isbn == "" and nr_bib == ""):
            error = "Er moet minstens 1 veld worden ingevuld"
        else:
            new_book = Boeken(titel=titel_boek,isbn=isbn,auteur=naam_auteur,afkorting_auteur=afkorting_auteur,categorie=categorie,nummer_jaartal_volgnummer=nr_bib)
            db.session.add(new_book)
            db.session.commit()
            succes = "Het boek is toegevoegd aan de database!"
        return render_template("beheer.html",succes=succes,error=error)
    return render_template('beheer.html')


#pagina's hieronder zijn enkel lijsten, hierop gebeuren geen acties deze laten enkel lijsten van boeken zien

@main.route('/boekenlijst',methods=['POST',"GET"])
@login_required
def boekenlijst():
    status_boek = False
    gevonden_boeken = Boeken.query.all()
    return render_template("boekenlijst.html",gevonden_boeken=gevonden_boeken)

@main.route('/uitgeleendlijst')
@login_required
def uitgeleendlijst():
    error = None
    all_leningen = Lenen.query.all()
    gevonden_boeken = Boeken.query.join(Lenen).filter(Lenen.LeenID == Boeken.LeenID).all()
    leningen_boek = Lenen.query.join(Boeken).filter(Lenen.BoekID == Boeken.BoekID).all()
    gevonden_lln = Leerlingen.query.join(Lenen).filter(Lenen.LeerlingID == Leerlingen.LeerlingID).all()
    print(gevonden_lln)
    if(gevonden_boeken == []):
        error = "Er zijn op dit moment geen boeken uitgeleend"
    
   
    return render_template('uitgeleendelijst.html',gevonden_lln=gevonden_lln,leningen_boek=leningen_boek,gevonden_boeken=gevonden_boeken,error=error)