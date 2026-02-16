import random
import tkinter as tk
from tkinter import messagebox
from collections import deque

# -------------------------------------------------------------
# CLASSE 1 : Gestion de la Configuration
# -------------------------------------------------------------
class ConfigJeu:
    """Contient toutes les constantes et configurations du jeu."""
    
    CHOIX_POSSIBLES = ["pierre", "feuille", "ciseaux"]
    EMOJIS = {
        "pierre": "🪨",
        "feuille": "📃",
        "ciseaux": "✂️"
    }
    COULEURS = {
        "Victoire": "green",
        "Défaite": "red",
        "Égalité": "blue"
    }
    
    BINDINGS = {
        'p': 'pierre',
        'f': 'feuille',
        'c': 'ciseaux'
    }
    
    POLICE_TITRE = ("Arial", 18, "bold")
    POLICE_STANDARD = ("Arial", 12)
    POLICE_RESULTAT = ("Arial", 30, "bold")
    
    def _init(self, manches_a_gagner): # CORREGIDO: __init_
        self.manches_a_gagner = manches_a_gagner

# -------------------------------------------------------------
# CLASSE 2 : Logique du Jeu
# -------------------------------------------------------------
class LogiquePFC:
    def _init(self, config): # CORREGIDO: __init_
        self.config = config
        self.score_utilisateur = 0
        self.score_ordinateur = 0
        self.round_count = 0
        self.jeu_actif = True
        self.historique = deque(maxlen=5)

    def determiner_gagnant(self, choix_user, choix_bot):
        if choix_user == choix_bot:
            return "Égalité 🤝", 0, "Égalité"
        elif (choix_user == "pierre" and choix_bot == "ciseaux") or \
             (choix_user == "ciseaux" and choix_bot == "feuille") or \
             (choix_user == "feuille" and choix_bot == "pierre"):
            return "Victoire 🎉!", 1, "Victoire"
        else:
            return "Défaite 😢", -1, "Défaite"

    def jouer_round(self, choix_utilisateur):
        if not self.jeu_actif:
            return None, None, "Jeu terminé", False

        self.round_count += 1
        choix_ordinateur = random.choice(self.config.CHOIX_POSSIBLES)
        
        message, point, cle_resultat = self.determiner_gagnant(choix_utilisateur, choix_ordinateur)
        
        if point == 1:
            self.score_utilisateur += 1
        elif point == -1:
            self.score_ordinateur += 1
            
        self.historique.appendleft((self.round_count, choix_utilisateur, choix_ordinateur, cle_resultat))
        
        # Verificar si alguien ganó después de este round
        gagnant = self.verifier_fin_de_partie()
        
        return choix_ordinateur, message, cle_resultat, self.jeu_actif

    def verifier_fin_de_partie(self):
        if self.score_utilisateur >= self.config.manches_a_gagner:
            self.jeu_actif = False
            return "Utilisateur"
        elif self.score_ordinateur >= self.config.manches_a_gagner:
            self.jeu_actif = False
            return "Ordinateur"
        return None

    def reinitialiser_etat(self):
        self.score_utilisateur = 0
        self.score_ordinateur = 0
        self.round_count = 0
        self.jeu_actif = True
        self.historique.clear()

# -------------------------------------------------------------
# CLASSE 3 : Interface Graphique
# -------------------------------------------------------------
class JeuPFC(tk.Tk):
    def _init(self, manches_a_gagner=3): # CORREGIDO: __init_
        super()._init() # CORREGIDO: __init_
        
        self.config = ConfigJeu(manches_a_gagner)
        self.logique = LogiquePFC(self.config)
        
        self.title("🪨📃✂️ Pierre - Feuille - Ciseaux")
        self.geometry("550x650") 
        self.resizable(False, False)
        
        self._creer_widgets()
        self._configurer_raccourcis_clavier()
        self._mettre_a_jour_affichage(message=f"Prêt ! Objectif : {self.config.manches_a_gagner} victoires.")
        
    def _creer_widgets(self):
        tk.Label(self, text="⚔ JEU : Pierre - Feuille - Ciseaux ⚔", font=self.config.POLICE_TITRE).pack(pady=10)

        frame_info = tk.Frame(self)
        frame_info.pack(pady=5)
        
        self.label_round = tk.Label(frame_info, font=self.config.POLICE_STANDARD)
        self.label_round.grid(row=0, column=0, padx=20)
        
        self.label_manches = tk.Label(frame_info, text=f"Objectif : {self.config.manches_a_gagner}", font=self.config.POLICE_STANDARD)
        self.label_manches.grid(row=0, column=1, padx=20)

        self.label_score = tk.Label(self, font=("Arial", 14, "bold"))
        self.label_score.pack(pady=5)

        self.label_result = tk.Label(self, text="", font=self.config.POLICE_RESULTAT)
        self.label_result.pack(pady=10)

        self.label_message = tk.Label(self, text="", font=("Arial", 14, "italic"))
        self.label_message.pack(pady=10)

        self.frame_boutons = tk.Frame(self)
        self.frame_boutons.pack(pady=15)

        self.boutons_choix = {}
        # CORRECCIÓN: Iteración segura de bindings para los botones
        for i, (touche, choix) in enumerate(self.config.BINDINGS.items()):
            btn = tk.Button(
                self.frame_boutons, 
                text=f"{self.config.EMOJIS[choix]} {choix.capitalize()} ({touche.upper()})", 
                font=self.config.POLICE_STANDARD, 
                width=15, 
                command=lambda c=choix: self.action_jouer(c)
            )
            btn.grid(row=0, column=i, padx=5)
            self.boutons_choix[choix] = btn

        tk.Label(self, text="--- Historique des 5 derniers rounds ---", font=("Arial", 12, "underline")).pack(pady=10)
        self.text_historique = tk.Text(self, height=5, width=65, font=("Courier", 10), state='disabled')
        self.text_historique.pack(pady=5)

        frame_controle = tk.Frame(self)
        frame_controle.pack(pady=20)

        tk.Button(frame_controle, text="🔄 Nouvelle Partie", font=self.config.POLICE_STANDARD,
                  command=self.reinitialiser, bg="#FFD700").grid(row=0, column=0, padx=10)
        tk.Button(frame_controle, text="❌ Quitter", font=self.config.POLICE_STANDARD,
                  command=self.quitter, bg="#FF6347").grid(row=0, column=1, padx=10)
        
    def _configurer_raccourcis_clavier(self):
        for touche, choix in self.config.BINDINGS.items():
            self.bind(touche.lower(), lambda event, c=choix: self.action_jouer(c))
            self.bind(touche.upper(), lambda event, c=choix: self.action_jouer(c))
            
    def _controler_boutons(self, etat):
        for btn in self.boutons_choix.values():
            btn.config(state=etat)

    def _mettre_a_jour_affichage(self, choix_utilisateur=None, choix_ordinateur=None, message="", cle_resultat=""):
        couleur = self.config.COULEURS.get(cle_resultat, "black")
        self.label_round.config(text=f"Round : {self.logique.round_count}")
        self.label_score.config(text=f"Score : Vous {self.logique.score_utilisateur} | Ordinateur {self.logique.score_ordinateur}")
        self.label_message.config(text=message, fg=couleur)
        
        if choix_utilisateur and choix_ordinateur:
            self.label_result.config(text=f"{self.config.EMOJIS[choix_utilisateur]} vs {self.config.EMOJIS[choix_ordinateur]}")
        else:
            self.label_result.config(text="") 

    def _mettre_a_jour_historique_gui(self):
        self.text_historique.config(state='normal')
        self.text_historique.delete('1.0', tk.END)
        for round_num, choix_u, choix_o, resultat in self.logique.historique:
            ligne = f"R{round_num}: Vous {self.config.EMOJIS[choix_u]} vs {self.config.EMOJIS[choix_o]} CPU -> {resultat}\n"
            self.text_historique.insert(tk.END, ligne)
        self.text_historique.config(state='disabled')
        
    def action_jouer(self, choix_utilisateur):
        if not self.logique.jeu_actif:
            return

        choix_ordinateur, message, cle_resultat, jeu_actif = self.logique.jouer_round(choix_utilisateur)
        self._mettre_a_jour_affichage(choix_utilisateur, choix_ordinateur, message, cle_resultat)
        self._mettre_a_jour_historique_gui()

        if not jeu_actif:
            gagnant = "L'Utilisateur" if self.logique.score_utilisateur > self.logique.score_ordinateur else "L'Ordinateur"
            message_final = f"FIN DE PARTIE ! {gagnant} remporte la victoire !"
            self.label_message.config(text=message_final, fg="purple")
            self._controler_boutons('disabled')
            messagebox.showinfo("FIN DE PARTIE", message_final)

    def reinitialiser(self):
        self.logique.reinitialiser_etat()
        self._mettre_a_jour_affichage(message=f"Nouvelle partie ! Objectif : {self.config.manches_a_gagner} victoires.")
        self._controler_boutons('normal')
        self._mettre_a_jour_historique_gui()

    def quitter(self):
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter ?"):
            self.destroy()

if _name_ == "_main": # CORREGIDO: __name_ y _main_
    app = JeuPFC(manches_a_gagner=5) 
    app.mainloop()