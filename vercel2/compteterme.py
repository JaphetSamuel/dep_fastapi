from fastapi import FastAPI , HTTPException
import requests
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np
import numpy_financial as npf
from datetime import date


import tracemalloc

# Activer tracemalloc
tracemalloc.start()


app = FastAPI()


#########################################################################################################""
def calculer_solde(df, inflation):
    import math
    import pandas as pd
    import datetime

    date_today = datetime.date.today()

    solde_aujourd_hui_list = []
    solde_inflation_list = []
    versement_cumul =[]

    for i in range(len(df)):
        taux_interet= df.iloc[i]['tauxInteret']
        date_ouverture = pd.to_datetime(df.iloc[i]['dateOuverture'], format='%Y-%m-%dT%H:%M:%SZ').date()
        date_cloture = pd.to_datetime(df.iloc[i]['dateCloture'], format='%Y-%m-%dT%H:%M:%SZ').date()
        m_versement = df.iloc[i]['montantVersment']
        periode = df.iloc[i]['periodiciteVersement']
        modalites_cloture_anticip = df.iloc[i]['modaliteClotureAnticipe']

        duree_jours = (date_today - date_ouverture).days

        if periode == 'mensuelle':
            nombre_periodes = duree_jours / 30
            taux_interet = taux_interet/12
        elif periode == 'trimestriel':
            nombre_periodes = duree_jours / 90
            taux_interet = taux_interet/4
        elif periode == 'semestriel':
            nombre_periodes = duree_jours / 180
            taux_interet = taux_interet / 3
        else:
            nombre_periodes = duree_jours / 360
            taux_interet = taux_interet / 1
        
#interet en cas d'anticipation
        if date_today < date_cloture:
            taux_interet = taux_interet * modalites_cloture_anticip
        #cumule des primes 
        Prime_cumulé =  m_versement* math.ceil(nombre_periodes)
        
        solde_aujourd_hui= 0
        for t in range(1, math.ceil(nombre_periodes) + 1):
            solde_aujourd_hui += m_versement * (1 + taux_interet) ** t

        solde_inflation = solde_aujourd_hui * (1 - inflation)

        solde_aujourd_hui_list.append(solde_aujourd_hui)
        solde_inflation_list.append(solde_inflation)
        versement_cumul.append(Prime_cumulé)
        
    new_solde = {'CumuledesVersements':versement_cumul ,'soldeaujourd-hui': solde_aujourd_hui_list, 'soldeinflation': solde_inflation_list}

    return new_solde


#########################################################################################################################


def Actifs_pro(df):
    import pandas as pd
    Denomination_de_societe_list = []
    Type_de_bien_list = []
    Valeur_parts_detenues_list = []
    
    somme_valeurs_parts = 0

    for i in range(len(df)):
        Denomination_de_societe = df.iloc[i]['libelle']
        Type_de_bien = df.iloc[i]['typeBien']
        Valeur_parts_detenues = df.iloc[i]['valeurPartsDetenus']

        Denomination_de_societe_list.append(Denomination_de_societe)
        Type_de_bien_list.append(Type_de_bien)
        Valeur_parts_detenues_list.append(Valeur_parts_detenues)
        
        somme_valeurs_parts += Valeur_parts_detenues
    


    Actifs_professionnels = {'somme':somme_valeurs_parts}


    return Actifs_professionnels

#############################################################################################################################""


def calculer_sommes_meubles_et_divers(df):
    
    import pandas as pd

    Valeur_acquisition_list=[]
    passifs_list=[]
    revenus_list=[]
    charges_list=[]
    
    somme_valeur_acquisition = 0
    somme_passifs = 0
    somme_revenus = 0
    somme_charges = 0

    for i in range(len(df)):
        Valeur_acquisition = df.iloc[i]['valeurAcquisition']
        passifs = df.iloc[i]['passifs']
        revenus = df.iloc[i]['revenus']
        charges = df.iloc[i]['charges']
        
        Valeur_acquisition_list.append(Valeur_acquisition)
        passifs_list.append(passifs)
        revenus_list.append(revenus)
        charges_list.append(charges)
        
        somme_valeur_acquisition += Valeur_acquisition
        somme_passifs += passifs
        somme_revenus += revenus
        somme_charges += charges
        
    revenu_net= somme_revenus-somme_passifs-somme_charges

    sommes_df ={
        'Somme des valeurs d\'acquisition': somme_valeur_acquisition,
        'Somme des passifs': somme_passifs,
        'Somme des revenus': somme_revenus,
        'Somme des charges': somme_charges,
        'Revenu net': revenu_net
    }

    return sommes_df

##########################################################################################################

def calculer_sommes_meubles_et_divers(df):
    
    import pandas as pd

    identifiant = []
    revenu = []
    
    

    for i in range(len(df)):
        identifiantbien = df.iloc[i]['identifiantBien']
        passifs = df.iloc[i]['passifs']
        revenus = df.iloc[i]['revenus']
        charges = df.iloc[i]['charges']
        
        revenu_net = revenus - charges - passifs
        
        revenu.append(revenu_net)
        identifiant.append(identifiantbien)
        
    resultat = {
        'identifiantBien': identifiant,
        'RevenuNet': revenu
    }

    return  resultat


def calculer_meubles_et_divers(df):
    
    import pandas as pd

    Valeur_acquisition_list=[]
    passifs_list=[]
    revenus_list=[]
    charges_list=[]
    
    somme_valeur_acquisition = 0
    somme_passifs = 0
    somme_revenus = 0
    somme_charges = 0

    for i in range(len(df)):
        Valeur_acquisition = df.iloc[i]['valeurAcquisition']
        passifs = df.iloc[i]['passifs']
        revenus = df.iloc[i]['revenus']
        charges = df.iloc[i]['charges']
        
        Valeur_acquisition_list.append(Valeur_acquisition)
        passifs_list.append(passifs)
        revenus_list.append(revenus)
        charges_list.append(charges)
        
        somme_valeur_acquisition += Valeur_acquisition
        somme_passifs += passifs
        somme_revenus += revenus
        somme_charges += charges
        
    revenu_net= somme_revenus-somme_passifs-somme_charges

    sommes_df ={
        'Somme des valeurs d\'acquisition': somme_valeur_acquisition,
        'Somme des passifs': somme_passifs,
        'Somme des revenus': somme_revenus,
        'Somme des charges': somme_charges,
        'Revenu net': revenu_net
    }

    return sommes_df



############################################################################################


def calculer_resultats_creances(df):
    import pandas as pd

    Encours = []
    preteurs = []
    Interets = []
    InteretsCourus = []

    for i in range(len(df)):
        preteur = df.iloc[i]['preteur']
        montant_initial = df.iloc[i]['montantInitial']
        montant_rembourse = df.iloc[i]['montantRembourse']
        taux_interet = df.iloc[i]['tauxInteret']  
        encours = df.iloc[i]['encours']
        identifiantclient = df.iloc[i]['identifiantClient']
        
    
        interet_couru = encours * (taux_interet/100)
        encour = encours*1
        Encours.append(int(encour))
        preteurs.append(preteur)
        Interets.append(int(taux_interet))
        InteretsCourus.append(int(interet_couru))
        
        
    resultats = { 
    'Preteurs' : preteurs,
    'Encours' : encour,
    'Interet' : Interets,
    'InteretsCourus': InteretsCourus
    }
    return  resultats

##########################################################################################################

def calculer_resultats_plus_value_cession(df):
    import pandas as pd
    resultats = []
    somme_montant=0

    for i in range(len(df)):
        cedant = df.iloc[i]['cedant']
        nature_bien = df.iloc[i]['natureBien']
        montant_plus_value = df.iloc[i]['montantPlusValue']
        frais_vente_associes = df.iloc[i]['montantFraisVenteAssocie']

        somme_montant+= montant_plus_value
    
    somme_montant1 = int(somme_montant)
    
    resultats_df= {
        'Total Plus Value': somme_montant1
    }

    return resultats_df

################################################################################################################

def plus_value_cession(df):
    import pandas as pd
    resultats = []
    bien = []
    somme_montant=0

    for i in range(len(df)):
        cedant = df.iloc[i]['cedant']
        nature_bien = df.iloc[i]['natureBien']
        montant_plus_value = df.iloc[i]['montantPlusValue']
        frais_vente_associes = df.iloc[i]['montantFraisVenteAssocie']

        somme_montant = montant_plus_value - frais_vente_associes
        resultats.append(somme_montant)
        bien.append(nature_bien)
        
    resultats_df = {
        'Total Plus Value':  resultats,
        'Bien': bien
    }

    return resultats_df

#################################################################################################

def capitalisation(df):
    import pandas as pd
    import datetime
    import math
    


    date_today = datetime.date.today()
    
    solde_aujourd_hui_list = []
    Cumule_prime = []
    Montant = []
    Contrat = []

    for i in range(len(df)):
        taux_interet = df.iloc[i]['interet']
        taux_interet= taux_interet/100
        periode_dure = df.iloc[i]['nombrePeriode']
        prime_periodique = df.iloc[i]['primePeriodique']
        duree_contrat = df.iloc[i]['dureeContrat']
        montant_assure = df.iloc[i]['montantAssurance']
        montant_avance = df.iloc[i]['montantAvance']
        contrat = df.iloc[i]['contrat']
        
        date_ouverture = pd.to_datetime(df.iloc[i]['dateSouscription'],format='%Y-%m-%dT%H:%M:%SZ').date()
        #date_cloture = pd.to_datetime(df.iloc[i]['dateCloture'],format='%Y-%m-%dT%H:%M:%SZ').date()
        #anticipation = df.iloc[i]['modaliteClotureAnticipe']

        #duree_contrat = (date_cloture - date_ouverture).days

        duree_jours = (date_today - date_ouverture).days

        periodicite = df.iloc[i]['periodiciteVersement'].lower()
        if 'mensuelle' in periodicite:
            versements_par_an = 12
            nombre_periodes =  duree_jours/30
            taux_interet_Periodique =  taux_interet/12
            #periode_dure = duree_contrat/30
        elif 'trimestrielle' in periodicite:
            versements_par_an = 4
            nombre_periodes =  duree_jours/90
            #periode_dure = duree_contrat/90
            taux_interet_Periodique =  taux_interet/4
        elif 'semestrielle' in periodicite:
            versements_par_an = 2
            nombre_periodes =  duree_jours/180
            #periode_dure = duree_contrat/180
            taux_interet_Periodique =  taux_interet/2
        else:
            versements_par_an = 1
            nombre_periodes =  duree_jours/360
            #periode_dure = duree_contrat/360
            taux_interet_Periodique =  taux_interet/1
            
         #cumule des primes 
        
        Contrat.append(contrat)
        
        Montant_payé = math.ceil(nombre_periodes)*prime_periodique
        
        #Capitalisation des prime 
        if nombre_periodes <= periode_dure:



            solde_aujourd_hui_list.append(0)
            
            Cumule_prime.append(int(Montant_payé))
            
            Montant.append(montant_assure)
            
            

            solde_aujourd_hui = 0   
            for t in range(1, math.ceil(nombre_periodes) + 1):
                solde_aujourd_hui += prime_periodique * (1 + taux_interet_Periodique) ** t
            
            solde_aujourd_hui_list.append(solde_aujourd_hui)
            Cumule_prime.append(int(Montant_payé))
            Montant.append(montant_assure)
    #solde = pd.DataFrame( solde_aujourd_hui_list, index=df['Contrat'], columns=['solde aujourd-hui','Primé Cumulé'])
    #solde = pd.DataFrame({'Montant aujourd-hui':solde_aujourd_hui_list ,'Primé Cumulé': Cumule_prime, 'Montant Assuré': Montant}, index=df['contrat'])
    solde = {'Montant_aujourd-hui':solde_aujourd_hui_list ,'Primé Cumulé': Cumule_prime, 'Montant Assuré': Montant, 'Contrat': Contrat}

    return solde

################################################################################################################################################

def evaluer_compte_courant(df):
    identifiant = []
    montant_solde = []
    interets_annuels = []
    solde_net_apres_charges = []
    detenteur = []
    
    for i in range(len(df)):
        numero_compte = df.iloc[i]['numeroCompte']
        montant_solde_val = df.iloc[i]['montantSolde']
        taux_interet = df.iloc[i]['tauxInteret']
        charge_fiscale_annuelle = df.iloc[i]['chargeFiscaleAnnuelle']
        est_detenu_par_client = df.iloc[i]['estDetenuParClient']
        autre_detenteur = df.iloc[i]['autreDetenteur']
        
        # Calcul des intérêts annuels et du solde net après charges fiscales
        interet_annuel = montant_solde_val * (taux_interet / 100)
        solde_net = montant_solde_val + interet_annuel - charge_fiscale_annuelle
        
        # Déterminer le détenteur
        detenteur_val = "Client" if est_detenu_par_client else autre_detenteur
        
        # Ajout des valeurs dans les listes
        identifiant.append(numero_compte)
        montant_solde.append(int(montant_solde_val))
        interets_annuels.append(int(interet_annuel))
        solde_net_apres_charges.append(solde_net)
        detenteur.append(detenteur_val)
    
    # Préparation du résultat sous forme de dictionnaire
    resultat = {
        'numeroCompte': identifiant,
        'montantSolde': montant_solde,
        'interetsAnnuels': interets_annuels,
        'soldeNetApresCharges': solde_net_apres_charges,
        'detenteur': detenteur
    }
    
    return resultat

#########################################################################################################################""""

def evaluer_autres_disponibilites(df):
    identifiant = []
    montant_solde = []
    interets_annuels = []
    solde_net_apres_charges = []
    detenteur = []
    type_actif = []
    devise = []
    libelle = []
    
    for i in range(len(df)):
        depositaire = df.iloc[i]['depositaire']
        montant_solde_val = df.iloc[i]['montantSolde']
        taux_interet = df.iloc[i]['tauxInteret']
        charge_fiscale_annuelle = df.iloc[i]['chargeFiscaleAnnuelle']
        type_actif_val = df.iloc[i]['typeActif']
        identifiant_client = df.iloc[i]['identifiantClient']
        est_detenu_par_client = df.iloc[i]['estDetenuParClient']
        autre_detenteur = df.iloc[i]['autreDetenteur']
        devise_val = df.iloc[i]['devise']
        libelle_val = df.iloc[i]['libelle']
        
        # Calcul des intérêts annuels et du solde net après charges fiscales
        interet_annuel = montant_solde_val * (taux_interet / 100)
        solde_net = montant_solde_val + interet_annuel - charge_fiscale_annuelle
        
        # Déterminer le détenteur
        detenteur_val = "Client" if est_detenu_par_client else autre_detenteur
        
        # Ajout des valeurs dans les listes
        identifiant.append(identifiant_client)
        montant_solde.append(int(montant_solde_val))
        interets_annuels.append(int(interet_annuel))
        solde_net_apres_charges.append(int(solde_net))
        detenteur.append(detenteur_val)
        type_actif.append(type_actif_val)
        devise.append(devise_val)
        libelle.append(libelle_val)
    
    # Préparation du résultat sous forme de dictionnaire
    resultat = {
        'identifiantClient': identifiant,
        'montantSolde': montant_solde,
        'interetsAnnuels': interets_annuels,
        'soldeNetApresCharges': solde_net_apres_charges,
        'detenteur': detenteur,
        'typeActif': type_actif,
        'devise': devise,
        'libelle': libelle
    }
    
    return resultat

########################################################################################################################################
# Fonction améliorée pour l'évaluation des passifs
def evaluer_passifs(df):
    identifiant = []
    libelle = []
    montant_initial = []
    capital_amorti = []
    taux_supporte = []
    taux_assurance = []
    periodicite_remboursement = []
    nombre_periode_amortissement = []
    periode_differee = []
    montant_restant_a_rembourser = []
    interets_cumules = []
    detenteur = []
    devise = []
    
    
    for i in range(len(df)):
        libelle_val = df.iloc[i]['libelle']
        montant_initial_val = df.iloc[i]['montantInitial']
        capital_amorti_val = df.iloc[i]['capitalAmorti']
        taux_supporte_val = df.iloc[i]['tauxSupporte']
        taux_assurance_val = df.iloc[i]['tauxAssurance']
        periodicite_remboursement_val = df.iloc[i]['periodiciteRemboursement']
        nombre_periode_amortissement_val = df.iloc[i]['nombrePeriodeAmortissement']
        periode_differee_val = df.iloc[i]['periodeDifferee']
        identifiant_client = df.iloc[i]['identifiantClient']
        est_detenu_par_client = df.iloc[i]['estDetenuParClient']
        autre_detenteur = df.iloc[i]['autreDetenteur']
        devise_val = df.iloc[i]['devise']
        
        # Calcul du montant restant à rembourser après amortissement
        montant_restant = montant_initial_val - capital_amorti_val
        
        # Calcul des intérêts cumulés selon le taux supporté
        interet_annuel = montant_restant * (taux_supporte_val / 100)
        interets_cumul = interet_annuel * nombre_periode_amortissement_val
        
        
        
        # Calcul du montant des assurances
        montant_assurance = montant_restant * (taux_assurance_val / 100)
        
        # Déterminer le détenteur
        detenteur_val = "Client" if est_detenu_par_client else autre_detenteur
        
        # Ajout des valeurs dans les listes
        identifiant.append(identifiant_client)
        libelle.append(libelle_val)
        montant_initial.append(int(montant_initial_val))
        capital_amorti.append(int(capital_amorti_val))
        taux_supporte.append(int(taux_supporte_val))
        taux_assurance.append(int(taux_assurance_val))
        periodicite_remboursement.append(periodicite_remboursement_val)
        nombre_periode_amortissement.append(int(nombre_periode_amortissement_val))
        periode_differee.append(int(periode_differee_val))
        montant_restant_a_rembourser.append(int(montant_restant))
        interets_cumules.append(int(interets_cumul))
        
        devise.append(devise_val)
    
    # Préparation du résultat sous forme de dictionnaire avec les informations complètes
    resultat = {
        'identifiantClient': identifiant,
        'libelle': libelle,
        'montantInitial': montant_initial,
        'capitalAmorti': capital_amorti,
        'tauxSupporte': taux_supporte,
        'tauxAssurance': taux_assurance,
        'periodiciteRemboursement': periodicite_remboursement,
        'nombrePeriodeAmortissement': nombre_periode_amortissement,
        'periodeDifferee': periode_differee,
        'montantRestantARembourser': montant_restant_a_rembourser,
        'interetsCumules': interets_cumules,
        'devise': devise
    }
    
    return resultat



def evaluer_creances(df):
    identifiant = []
    libelle = []
    nature_creance = []
    precision_nature = []
    montant_creance = []
    identifiant_client = []
    detenteur = []
    devise = []
    montant_creance_evalué = []
    
    for i in range(len(df)):
        libelle_val = df.iloc[i]['libelle']
        nature_creance_val = df.iloc[i]['natureCreance']
        precision_nature_val = df.iloc[i]['precisionNature']
        montant_creance_val = df.iloc[i]['montantCreance']
        identifiant_client_val = df.iloc[i]['identifiantClient']
        est_detenu_par_client = df.iloc[i]['estDetenuParClient']
        autre_detenteur = df.iloc[i]['autreDetenteur']
        devise_val = df.iloc[i]['devise']
        
        # Calcul de l'évaluation de la créance, on peut intégrer une logique spécifique ici
        # Exemple simplifié: évaluer la créance en fonction de la devise (conversion de devise)
        # Si la devise n'est pas en EUR, appliquer un taux de conversion (hypothétique)
        taux_conversion = 1  # Taux de conversion par défaut (pour EUR)
        if devise_val != "EUR":
            taux_conversion = 1.2  # Hypothèse: taux de conversion fictif pour une autre devise
        
        montant_creance_evalué_val = montant_creance_val * taux_conversion
        
        # Vérifier si la créance est détenue par le client ou un autre détenteur
        detenteur_val = "Client" if est_detenu_par_client else autre_detenteur
        
        # Ajouter les résultats dans les listes
        identifiant.append(identifiant_client_val)
        libelle.append(libelle_val)
        nature_creance.append(nature_creance_val)
        precision_nature.append(precision_nature_val)
        montant_creance.append(int(montant_creance_val))
        identifiant_client.append(identifiant_client_val)
        detenteur.append(detenteur_val)
        devise.append(devise_val)
        montant_creance_evalué.append(int(montant_creance_evalué_val))
    
    # Résultat final sous forme de dictionnaire
    resultat = {
        'identifiantClient': identifiant,
        'libelle': libelle,
        'natureCreance': nature_creance,
        'precisionNature': precision_nature,
        'montantCreance': montant_creance,
        'identifiantClient': identifiant_client,
        'detenteur': detenteur,
        'devise': devise,
        'montantCreanceEvalué': montant_creance_evalué
    }
    
    return resultat

#####################################################################################################################################

Token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiJjMmY0NzQ4Ni05MGZkLTRhODEtYTc4YS02YjM0YmVlYzU4NDEiLCJqdGkiOiIzZjI3MDNjNS1jODZhLTRiMzYtOWFmZS0xNzc5ZGExNTUyYzUiLCJnaXZlbl9uYW1lIjoiTUFSQ0VMIEFORUUiLCJmYW1pbHlfbmFtZSI6Ik1BUkNFTCBBTkVFIiwiZm9uY3Rpb24iOiJFdmFsdWF0ZXVyIEZpbmFuY2llciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL21vYmlsZXBob25lIjoiMDAyMjUwNzU3NTU2Njg1IiwiZW1haWwiOiJtYXJjZWwuYW5lZUByaXNrbG9naWNzY29uc3VsdC5jb20iLCJyb2xlIjoiQ29udHLDtGxldXIgRmluYW5jaWVyIiwiVmFsZXVyTW9iaWxpZXJlIjpbIlVwZGF0ZSIsIkNyZWF0ZSIsIlJlYWQiLCJEZWxldGUiXSwiQ29tcHRlRGVwb3REQVQiOlsiRGVsZXRlIiwiUmVhZCIsIkNyZWF0ZSIsIlVwZGF0ZUFtb3VudCIsIlVwZGF0ZSJdLCJBdXRyZURpc3BvbmliaWxpdGUiOlsiVXBkYXRlQW1vdW50IiwiVXBkYXRlIiwiQ3JlYXRlIiwiUmVhZCIsIkRlbGV0ZSJdLCJDcmVhbmNlVGllcnMiOlsiQ3JlYXRlIiwiVXBkYXRlRGVsYWlDcmVhbmNlIiwiVXBkYXRlQW1vdW50IiwiVXBkYXRlIiwiUmVhZCIsIkRlbGV0ZSJdLCJBdXRyZUNyZWFuY2UiOlsiVXBkYXRlIiwiVXBkYXRlRGVsYWlDcmVhbmNlIiwiVXBkYXRlQW1vdW50IiwiQ3JlYXRlIiwiRGVsZXRlIiwiUmVhZCJdLCJCaWVuQ2Vzc2lvbiI6WyJEZWxldGUiLCJDcmVhdGUiLCJVcGRhdGUiLCJSZWFkIl0sIkhvcnNCaWxhbiI6WyJVcGRhdGUiLCJSZWFkIiwiRGVsZXRlIiwiQ3JlYXRlIl0sIkJpZW5Gb25jaWVyIjpbIlJlYWQiLCJVcGRhdGUiLCJEZWxldGUiLCJDcmVhdGUiXSwiTWV1YmxlRGl2ZXIiOlsiQ3JlYXRlIiwiRGVsZXRlIiwiVXBkYXRlIiwiUmVhZCJdLCJSZXZlbnVzIjpbIlVwZGF0ZSIsIlJlYWQiLCJDcmVhdGUiLCJEZWxldGUiXSwiRG9zc2llckNsaWVudCI6IlJlYWQiLCJCaWxhblBhdHJpbW9uaWFsIjoiUmVhZCIsIkV2YWx1YXRpb25QZXJmb3JtYW5jZSI6IlJlYWQiLCJDaGFyZ2VzIjoiUmVhZCIsIkFzc3VyYW5jZSI6WyJEZWxldGUiLCJDcmVhdGUiLCJSZWFkIiwiVXBkYXRlIl0sIkhlcml0YWdlRG9uYXRpb24iOlsiVXBkYXRlIiwiRGVsZXRlIiwiQ3JlYXRlIiwiUmVhZCJdLCJQYXNzaWYiOlsiRGVsZXRlIiwiQ3JlYXRlIiwiVXBkYXRlIiwiUmVhZCJdLCJBdm9pck5vbkZpbmFuY2llciI6IlVwZGF0ZUFtb3VudCIsIkFjdGlmUHJvZmVzc2lvbm5lbCI6WyJVcGRhdGVBbW91bnQiLCJSZWFkIiwiRGVsZXRlIiwiQ3JlYXRlIiwiVXBkYXRlIl0sIkF1dHJlQXZvaXJOb25GaW5hbmNpZXIiOlsiVXBkYXRlIiwiQ3JlYXRlIiwiUmVhZCIsIkRlbGV0ZSJdLCJEb25hdGlvbkFudGVyaWV1cmUiOlsiQ3JlYXRlIiwiRGVsZXRlIiwiUmVhZCIsIlVwZGF0ZSJdLCJEYXNoYm9yZEJ1ZGdldCI6IlJlYWQiLCJHZXN0aW9uRG9jdW1lbnRhaXJlIjoiUmVhZCIsIkRvbmF0aW9uQWN0dWVsbGUiOiJSZWFkIiwibmJmIjoxNzMyNzU0MzQyLCJleHAiOjE3MzI3NTQ2NDIsImlhdCI6MTczMjc1NDM0MiwiaXNzIjoiaHR0cHM6Ly9iYWNrLnNncC5hdGxhbnRpc3MtY2kuY29tL2F1dGgtdGVzdCIsImF1ZCI6Imh0dHBzOi8vc2dwLmt5cmlhLWNzLm9yZyJ9.kOKswjHdv3eOOeSpZ1tiFiS5vcdicqYtrTO98ByHadU"
#######################################################################################################################################





####################################################################################################################################""

url ='https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/comptes-termes'

headers = {
        'Authorization': f'Bearer {Token}'
    }

response = requests.get(url, headers=headers)
response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
external_data = response.json()
data1 = external_data['payLoad']


@app.post("/CompteaTerme")
def EvaluerCompteaTerme_endpoint(inflation):
    inflation = float(inflation)
    df = pd.DataFrame(data1)
    df_ = df[['numeroCompte','tauxInteret','dateOuverture','dateCloture','montantVersment','periodiciteVersement','montantSolde','modaliteClotureAnticipe']]
    resultat = calculer_solde(df_,inflation)
    #encrypted_result = encrypt_json(resultat)
    return resultat


#################################################################################################################
url ='https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/biens-professionnels'

headers = {
        'Authorization': f'Bearer {Token}'
    }

response = requests.get(url, headers=headers)
response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
external_data = response.json()
data2 = external_data['payLoad']


@app.post("/biens-professionnels")
def EvaluerbiensProfessionnels_endpoint():
    df_ = pd.DataFrame(data2)
    resultat = Actifs_pro(df_)
    
    #encrypted_result1 = encrypt_json(resultat)
    return resultat
#############################################################################################################

url = 'https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/biens-immobiliers'
headers = {
        'Authorization': f'Bearer {Token}'
    }

response = requests.get(url, headers=headers)
response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
external_data = response.json()
data3 = external_data['payLoad']


@app.post("/biens-meubles")
def EvaluerBiensmeubles_endpoint():
    df_ = pd.DataFrame(data3)
    resultat = calculer_sommes_meubles_et_divers(df_)
    print(resultat)
    #encrypted_result2 = encrypt_json(resultat)
    return resultat

@app.post("/biens-meubles/divers")
def Evalauerbiensmeubles_endpoint():
    df_ = pd.DataFrame(data3)
    resultat = calculer_meubles_et_divers(df_)
    print(resultat)
    #encrypted_result3 = encrypt_json(resultat)
    return resultat


#############################################################################################################
url = 'https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/creance-tiers' 



headers = {
        'Authorization': f'Bearer {Token}'
    }

response = requests.get(url, headers=headers)
response.raise_for_status()  
external_data = response.json()
data4 = external_data['payLoad']

@app.post("/creance-tiers")
def Evaluercreancetiers_endpoint():
    df_ = pd.DataFrame(data4)
    resultat =calculer_resultats_creances(df_)
    
    #encrypted_result4 = encrypt_json(resultat)
    return resultat


#print(calculer_resultats_creances(data4))



###########################################################################################################################################
url = 'https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/bien-cession'
headers = {
        'Authorization': f'Bearer {Token}'
    }
response = requests.get(url, headers=headers)
response.raise_for_status()  
external_data = response.json()
data5 = external_data['payLoad']

@app.post("/bien-cession")
def Evaluerbiencession_endpoint():
    df_ = pd.DataFrame(data5)
    resultat =calculer_resultats_plus_value_cession(df_)
    
    #encrypted_result5 = encrypt_json(resultat)
    return resultat


@app.post("/cession/plus_value")
def EvaluerPlusvalueCession_endpoint():
    df_ = pd.DataFrame(data5)
    resultat =plus_value_cession(df_)
    
    #encrypted_result6 = encrypt_json(resultat)
    return resultat



###########################################################################################################################################
url = 'https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/produits-assurances'
headers = {
        'Authorization': f'Bearer {Token}'
    }
response = requests.get(url, headers=headers)
response.raise_for_status()  
external_data = response.json()
data6 = external_data['payLoad']

@app.post("/capitalisation",response_model = dict)
def EcaluerAssurancecapitalisation_endpoint():
    df_ = pd.DataFrame(data6)
    resultat =capitalisation(df_)
    
    #encrypted_result7 = encrypt_json(resultat)
    return resultat

###############################################################################################################""
url = 'https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/comptes-courants'
headers = {
        'Authorization': f'Bearer {Token}'
    }
response = requests.get(url, headers=headers)
response.raise_for_status()  
external_data = response.json()
data7 = external_data['payLoad']


@app.post("/evaluer-compte-courant")
def evaluer_compte_courant_endpoint():
    df_ = pd.DataFrame(data7)  
    resultat = evaluer_compte_courant(df_)
    #encrypted_result = encrypt_json(resultat)  # Encryptage des résultats avant retour
    return resultat

print(evaluer_compte_courant_endpoint())

################################################################################################""
url = 'https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/autres-disponibilites'
headers = {
        'Authorization': f'Bearer {Token}'
    }
response = requests.get(url, headers=headers)
response.raise_for_status()  
external_data = response.json()
data8 = external_data['payLoad']
data8 = pd.DataFrame(data8)

@app.post("/evaluer-autres-disponibilites")
def evaluer_autres_disponibilites_endpoint():
    df_ = pd.DataFrame(data8)  
    resultat = evaluer_autres_disponibilites(df_)
    #encrypted_result = encrypt_json(resultat)  
    return resultat



###########################################################################################################
url =  'https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/passifs'
headers = {
        'Authorization': f'Bearer {Token}'
    }
response = requests.get(url, headers=headers)
response.raise_for_status()  
external_data = response.json()
data9 = external_data['payLoad']
data9 = pd.DataFrame(data9)


@app.post("/evaluer-passifs")
def evaluer_passifs_endpoint():
    df_ = pd.DataFrame(data9) 
    resultat = evaluer_passifs(df_)
    #encrypted_result = encrypt_json(resultat)  # Encryption des résultats avant retour
    return resultat

#####################################################################################################################
url =  'https://back.sgp.atlantiss-ci.com/test/api/evaluation-performances/creances-autres'
headers = {
        'Authorization': f'Bearer {Token}'
    }
response = requests.get(url, headers=headers)
response.raise_for_status()  
external_data = response.json()
data10 = external_data['payLoad']
data10 = pd.DataFrame(data10)


@app.post("/evaluer-creance-autre")
def evaluer_creances_autre_endpoint():
    df_ = pd.DataFrame(data10)  # data3 contient les données d'exemple
    resultat = evaluer_creances(df_)
    
    return resultat


@app.get("/")
def azert():
    az = {'mot': 'hello world'}

    return az


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)