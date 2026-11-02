from psychopy import visual, event, core

def afficher_consignes_entrainement1(win, image_path_entrainement):
    """
    Affiche l’image des consignes et un texte d’introduction.
    :param win: fenêtre PsychoPy
    :param image_path: chemin de l'image à afficher
    """
    # Texte avant l'image
    texte_avant_image_entrainement = (
        "• Flèche droite : Sens horaire\n\n"
        "• Flèche gauche : Sens antihoraire\n\n"
        "• Flèche du bas : Valider réponse\n\n"
    )

    # Texte après l'image
    texte_apres_image_entrainement = (
        "Appuyez sur la touche 'Espace' pour commencer un essai pour vous familiariser avec la tâche"
    )

    # Créer les éléments visuels
    titre = visual.TextStim(win, text="Démo", color='black', height=40, bold=True, pos=(0, 365), font ='Arial')
    texte_avant_image_entrainement = visual.TextStim(win, text=texte_avant_image_entrainement, color='black', bold=True, height=30, pos=(0, 155), wrapWidth=1000, font ='Arial', alignText='left', anchorHoriz='center')
    consigne_image_entrainement = visual.ImageStim(win, image=image_path_entrainement, size=(550, 425), pos=(0, -150))
    texte_apres_image_entrainement = visual.TextStim(win, text=texte_apres_image_entrainement, color='black', height=20, pos=(0, -470), wrapWidth=1000, font ='Arial')

    # Affichage
    titre.draw()
    texte_avant_image_entrainement.draw()
    consigne_image_entrainement.draw()
    texte_apres_image_entrainement.draw()
    win.flip()

    # Attente
    event.waitKeys(keyList=['space'])

def afficher_consignes_entrainement2(win):
    """
    Affiche des consignes supplémentaires avant de commencer le test.
    :param win: fenêtre PsychoPy
    """
    texte_entrainement2 = (
        "Vous allez maintenant commencer l'entrainement.\n"
        "L'entrainement durera environ 5 minutes.\n\n\n" 
        "Essayez de répondre"
    )

    texte_gras_entrainement2 = (
        "le plus rapidement et le plus précisément possible."
    )

    texte_entrainement_continuer = (
        "Appuyez sur la touche 'Espace' pour commencer l'entrainement"
    )

    titre = visual.TextStim(win, text="Entrainement", color='black', height=40, bold=True, pos=(0, 365), font ='Arial')
    texte_entrainement2 = visual.TextStim(win, text=texte_entrainement2, color='black', height=30, pos=(0, 0), wrapWidth=1000, font='Arial',alignText='left', anchorHoriz='center')
    texte_gras_entrainement2 = visual.TextStim(win, text=texte_gras_entrainement2, color='black', height=30, pos=(295, -69), wrapWidth=1000, font='Arial', alignText='left', anchorHoriz='center', bold=True)
    texte_entrainement_continuer = visual.TextStim(win, text=texte_entrainement_continuer, color='black', height=20, pos=(0, -470), wrapWidth=1000, font='Arial')

    # Affichage des consignes supplémentaires
    titre.draw()
    texte_entrainement2.draw()
    texte_gras_entrainement2.draw()
    texte_entrainement_continuer.draw()
    win.flip()

    # Attente de l'utilisateur
    event.waitKeys(keyList=['space'])




def afficher_consignes_test_2(win, image_path_test2):

    texte_avant_image_test2 = (
        "Le temps de réponse est limité. Essayez donc de répondre avant la fin du temps imparti.\n\n"
        "Mais, ne choisissez pas une réponse au hasard.\n"
    )

    texte_avant_image_test2_gras = ("Soyez aussi rapide et précis que possible."
    )

    texte_apres_image_test2 = (

        "Appuyez sur la touche 'Espace' pour continuer\n\n"
    )


    titre = visual.TextStim(win, text="Test", color='black', height=40, bold=True, pos=(0, 385), font ='Arial')
    texte_avant_image_test2 = visual.TextStim(win, text=texte_avant_image_test2, color='black', height=27, pos=(100, 210), wrapWidth=1200, font='Arial', alignText='left', anchorHoriz='center')
    texte_avant_image_test2_gras = visual.TextStim(win, text=texte_avant_image_test2_gras, color='black', height=27, pos=(100, 95), wrapWidth=1200, font='Arial', alignText='left', anchorHoriz='center', bold=True)
    texte_apres_image_test2 = visual.TextStim(win, text=texte_apres_image_test2, color='black', height=20, pos=(0, -470), wrapWidth=1000, font='Arial')
    consigne_image_test2 = visual.ImageStim(win, image=image_path_test2, size=(500, 400), pos=(-10, -140))

    # Affichage des consignes supplémentaires
    titre.draw()
    texte_avant_image_test2.draw()
    texte_avant_image_test2_gras.draw()
    consigne_image_test2.draw()
    texte_apres_image_test2.draw()
    win.flip()

    # Attente de l'utilisateur
    event.waitKeys(keyList=['space'])

def afficher_consignes_test_3(win, image_path_test3):

    texte_avant_image_test3_gras = (
        "Vous devez atteindre un niveau de performance minimum.\n\n"
    )
    
    texte_avant_image_test3 = (
        "Votre performance doit être proche ou meilleure que la performance moyenne des autres participants.\n"
    )


    texte_apres_image_test3 = (
        "Appuyez sur la touche 'Espace' pour continuer\n\n"
    )

    titre = visual.TextStim(win, text="Test", color='black', height=40, bold=True, pos=(0, 385), font ='Arial')
    texte_avant_image_test3_gras = visual.TextStim(win, text=texte_avant_image_test3_gras, color='black', height=27, pos=(100, 210), wrapWidth=1200, font='Arial', alignText='left', anchorHoriz='center', bold = True,)
    texte_avant_image_test3 = visual.TextStim(win, text=texte_avant_image_test3, color='black', height=27, pos=(125, 115), wrapWidth=1250, font='Arial', alignText='left', anchorHoriz='center')
    texte_apres_image_test3 = visual.TextStim(win, text=texte_apres_image_test3, color='black', height=20, pos=(0, -470), wrapWidth=1000, font='Arial')
    consigne_image_test3 = visual.ImageStim(win, image=image_path_test3, size=(500, 400), pos=(-35, -140))

    # Affichage des consignes supplémentaires
    titre.draw()
    texte_avant_image_test3_gras.draw()
    texte_avant_image_test3.draw()
    consigne_image_test3.draw()
    texte_apres_image_test3.draw()
    win.flip()

    # Attente de l'utilisateur
    event.waitKeys(keyList=['space'])

def afficher_perf_moyenne(win, success_percentage,success_percentage_groupe ): 
    
    texte_perf_moyenne = (
        f"Votre performance moyenne est :\n"
        f"{success_percentage}% de réponses correctes.\n\n"
        "La performance moyenne est :\n"
        f"{success_percentage_groupe}% de réponses correctes.\n\n"
    )

    texte_perf_moyenne = visual.TextStim(win, text=texte_perf_moyenne, color='black', height=30, pos=(0, 0), wrapWidth=1000, font='Arial')
    sous_titre = visual.TextStim(win, text="Appuyez sur la touche 'Espace' pour continuer", color='black', height=20, pos=(0, -470), font ='Arial')
    
    texte_perf_moyenne.draw()
    sous_titre.draw()
    win.flip()

    event.waitKeys(keyList=['space'])