import json
import os
import random
import string
import tkinter as tk
from tkinter import messagebox, ttk

FICHIER = "candidats.json"

p = "qwerty"

def charger_donnees():
    if os.path.exists(FICHIER) == False:
        return []
    fichier = open(FICHIER, "r")
    contenu = json.load(fichier)
    fichier.close()
    return contenu


def sauvegarder_donnees(candidats):
        fichier = open(FICHIER, "w")
        json.dump(candidats, fichier)
        fichier.close()

def ressource_path(r_path):
    try:
        b_path = sys._MEIPASS
    except Exception:
        b_path = os.path.abspath(".")
        return os.path.join(b_path, r_path)

class AppCandidats:
    def __init__(self, root):
        self.root = root
        icon_p = ressource_path("icon.ico")
        self.root.iconbitmap(icon_p)
        self.root.title("Système de Gestion des Candidats")
        self.root.geometry("1100x600")
        self.root.configure(bg="#2c3e50")

        self.candidats = charger_donnees()

        self.sidebar = tk.Frame(self.root, bg="#1a252f", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="MENU", fg="white", bg="#1a252f", font=("Arial", 14, "bold")).pack(pady=20)

        boutons = [
            ("Ajouter", self.afficher_formulaire),
            ("Liste Complète", self.afficher_password),
            ("Rechercher / Suppr", self.afficher_recherche),
            ("Quitter", self.root.quit)
        ]

        for texte, commande in boutons:
            tk.Button(self.sidebar, text=texte, command=commande, bg="#34495e", fg="white",
                      font=("Arial", 11), relief="flat", activebackground="#3498db",
                      cursor="hand2").pack(fill="x", pady=5, padx=10, ipady=8)

        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.afficher_accueil()

    def vider_ecran(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def afficher_accueil(self):
        self.vider_ecran()
        tk.Label(self.main_frame, text="Gestion des Dossiers Candidats", bg="#ecf0f1",
                 font=("Arial", 24, "bold"), fg="#2c3e50").pack(pady=100)
        tk.Label(self.main_frame, text="Sélectionnez une option dans le menu de gauche.",
                 bg="#ecf0f1", font=("Arial", 12), fg="#7f8c8d").pack()



    def afficher_formulaire(self):
        global prochain_id
        self.vider_ecran()
        caracteres = string.ascii_uppercase + string.digits
        while True:
            prochain_id = ''.join(random.choices(caracteres, k=7))
            id_deja_pris = False
            for c in self.candidats:
                if c["id"] == prochain_id:
                    id_deja_pris = True
                    break
            if id_deja_pris == False:
                break

        container = tk.Frame(self.main_frame, bg="#ecf0f1")
        container.pack(pady=30)

        tk.Label(container, text=f"Ajouter Candidat (ID : {prochain_id})", font=("Arial", 16, "bold"),
                 bg="#ecf0f1").grid(row=0, columnspan=2, pady=20)

        fields = ["Nom", "Prénom", "Âge", "Sexe (M/F)"]
        self.entries = {}

        for i, field in enumerate(fields):
            tk.Label(container, text=field, bg="#ecf0f1", font=("Arial", 11)).grid(row=i + 1, column=0, sticky="w",
                                                                                   pady=5)
            ent = tk.Entry(container, font=("Arial", 11), width=30)
            ent.grid(row=i + 1, column=1, pady=5, padx=10)
            self.entries[field] = ent

        tk.Label(container, text="Niveau", bg="#ecf0f1", font=("Arial", 11)).grid(row=5, column=0, sticky="w", pady=5)
        self.combo_niveau = ttk.Combobox(container, values=["CEP", "BEPC", "PROBATOIRE", "BAC", "LICENCE", "MASTER"],
                                         state="readonly", width=28)
        self.combo_niveau.grid(row=5, column=1, pady=5, padx=10)
        self.combo_niveau.set("CEP")

        tk.Button(container, text="Enregistrer", bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                  command=lambda: self.valider_ajout(prochain_id)).grid(row=6, columnspan=2, pady=20, ipady=5,
                                                                        sticky="ew")

    def valider_ajout(self, identifiant):

        def montrer_id(prochain_id):
            fen = tk.Toplevel()
            fen.title("Votre ID")
            entry = tk.Entry(fen, width=40)
            entry.insert(0, str(prochain_id))
            entry.config(state="readonly")
            entry.pack(pady=5)
            def copier():
                fen.clipboard_clear()
                fen.clipboard_append(str(prochain_id))
                fen.update()
                messagebox.showinfo("Copié", "ID copié dans le presse-papiers !")

            bouton = tk.Button(fen, text="Copier", command=copier)
            bouton.pack(pady=5)

        nom = self.entries["Nom"].get().strip().upper()
        prenom = self.entries["Prénom"].get().strip().capitalize()
        age_str = self.entries["Âge"].get().strip()
        sexe = self.entries["Sexe (M/F)"].get().strip().upper()
        niveau = self.combo_niveau.get()
        if nom.isdigit() or prenom.isdigit() :
            messagebox.showwarning("Erreur", "Le nom et le prenom ne peuvent être constitués uniquement des chiffres !")
            return
        try:
            age = int(age_str)
            if age < 18 or age > 33:
                messagebox.showwarning("Âge", "Âge minimum requis : 18 ans."
                                              " Âge maximum requis : 33 ans.")
                return
        except:
            messagebox.showerror("Erreur", "L'âge doit être un nombre.")
            return

        if not nom or not prenom or not age_str:
            messagebox.showwarning("Erreur", "Tous les champs sont obligatoires.")
            return
        if sexe not in ['M', 'F']:
            messagebox.showwarning("Sexe", "Veuillez entrer M ou F.")
            return

        nouveau = {"id": str(identifiant), "nom": nom, "prenom": prenom, "age": age, "sexe": sexe, "niveau": niveau}
        self.candidats.append(nouveau)
        sauvegarder_donnees(self.candidats)
        messagebox.showinfo("Succès", "Candidat ajouté !")
        montrer_id(prochain_id)
        self.afficher_accueil()

        def executer_recherche(self, critere):
            critere = critere.strip()
            if not critere: return
            resultats = [c for c in self.candidats if c["id"] == int(critere) ]
            if resultats:
                self.afficher_tout(resultats)
            else:
                messagebox.showinfo("Info", "Veuillez un ID !")
        self.afficher_accueil()


    def afficher_tout(self, data_list=None):
        self.vider_ecran()
        data = data_list if data_list is not None else self.candidats

        tk.Label(self.main_frame, text="Liste des Candidats", font=("Arial", 18, "bold"), bg="#ecf0f1",
                 fg="#2c3e50").pack(pady=10)

        cols = ("ID", "Nom", "Prénom", "Âge", "Sexe", "Niveau")
        tree = ttk.Treeview(self.main_frame, columns=cols, show="headings")

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for c in data:
            tree.insert("", "end", values=(c["id"], c["nom"], c["prenom"], c["age"], c["sexe"], c["niveau"]))

        tree.pack(fill="both", expand=True, padx=20, pady=10)

    def afficher_password(self):
        self.vider_ecran()
        container = tk.Frame(self.main_frame, bg="#ecf0f1")
        container.pack(pady=20)

        tk.Label(container, text="Mot de passe administrateur", font=("Arial", 12), bg="#ecf0f1").pack()
        ent_search = tk.Entry(container, font=("Arial", 12), width=30)
        ent_search.pack(pady=10)

        btn_frame = tk.Frame(container, bg="#ecf0f1")
        btn_frame.pack()

        tk.Button(btn_frame, text="Confirmer", bg="#3498db", fg="white",
                  command=lambda: self.executer_password(ent_search.get())).pack(side="left", padx=5)

    def afficher_recherche(self):
            self.vider_ecran()
            container = tk.Frame(self.main_frame, bg="#ecf0f1")
            container.pack(pady=20)

            tk.Label(container, text="Rechercher / Supprimer par ID", font=("Arial", 12), bg="#ecf0f1").pack()
            ent_search = tk.Entry(container, font=("Arial", 12), width=30)
            ent_search.pack(pady=10)

            btn_frame = tk.Frame(container, bg="#ecf0f1")
            btn_frame.pack()

            tk.Button(btn_frame, text="Rechercher", bg="#3498db", fg="white",
                      command=lambda: self.executer_recherche(ent_search.get())).pack(side="left", padx=5)

            tk.Button(btn_frame, text="Supprimer l'ID", bg="#e74c3c", fg="white",
                      command=lambda: self.executer_suppression(ent_search.get())).pack(side="left", padx=5)

    def executer_password(self, password):
        if password == p:
            self.afficher_tout()
        else:
            messagebox.showinfo("Info", " Mot de passe incorrect  !")

    def executer_recherche(self, critere):
        critere = critere.strip().upper()
        if not critere: return
        resultats = [c for c in self.candidats if c["id"] == critere]
        if resultats:
            self.afficher_tout(resultats)
        else:
            messagebox.showinfo("Info", "Veuillez un ID !")


    def executer_suppression(self, identifiant):
        for c in self.candidats:
            if c["id"] == identifiant.strip().upper():
                if messagebox.askyesno("Confirmation", f"Supprimer {c['nom']} ?"):
                    self.candidats.remove(c)
                    sauvegarder_donnees(self.candidats)
                    self.afficher_accueil()
                return
        messagebox.showwarning("Erreur", "ID introuvable.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppCandidats(root)
    root.mainloop()