from Nancy import Categorie,Livre,db
nbre=int(input("combien de categorie voulez vou entrer"))
for i in range(nbre):
    une_categorie= Categorie(input("veuillez entrer le libelle de votre categorie:"))
    db.session.add(une_categorie)
    db.session.commit()
print("toute les insertions de categorie ont été faites")
nbr=int(input("combien de livres voulez vous entrez par categorie"))
for i in range(1,nbre+1):
    for i in  range(nbr):
        titre = input(f"Veuillez entrer le titre de la categorie {i} :")
        auteur= input("Veuillez entrer le auteur de ce titre:")
        editeur = input("Veuillez entrer l'editeur de ce titre' :")
        date= input("veuillez entrer la date:")
        isbn=input("veuillez saisir le code isbn")
        livre=Livre(isbn,titre,date,auteur,editeur,i)
        db.session.add(livre)
        db.session.commit()
print("toute les insertions de livre ont été faites")
print("toute les insertions ont été faites")

