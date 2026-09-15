# -*- coding: utf-8 -*-
"""
Banque de questions du quiz "Gestion de projet IA" (support v1.0, 7 parties).
4 modules x 20 questions. Chaque question : un enonce, la bonne reponse,
3 distracteurs plausibles, et une explication.

Regles de conception appliquees (verifiees par check_questions.py) :
- 4 propositions, 1 seule vraie ;
- la bonne reponse n'est jamais la proposition la plus longue ;
- distracteurs du meme registre et de longueur comparable a la bonne
  reponse (pas de "bonne reponse evidente") ;
- la position de la bonne reponse suit un motif equilibre par module,
  DIFFERENT de celui du quiz "Conduite du changement" ;
- pas de distracteur manifestement absurde.

Le placement de la bonne reponse est deterministe (motif PLACEMENT + seed fixe)
pour que l'ordre servi au client soit stable entre deux redemarrages.
"""

import random

# Motif de placement de la bonne reponse par question (index 0..3 = A..D).
# Volontairement different du quiz adoption. Sur 20 questions : A:5 B:5 C:5 D:5.
PLACEMENT = [1, 3, 0, 2, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 0, 2, 1, 3, 0, 2]

RAW = {
    "m1": {
        "title": "Module 1 — Comprendre et cadrer un projet IA",
        "questions": [
            {
                "q": "Quelle part des projets IA ne passent jamais en production ou n'apportent pas la valeur attendue (ordres de grandeur Gartner, McKinsey) ?",
                "correct": "50 à 80 %",
                "distractors": ["15 à 25 %", "30 à 45 %", "Plus de 95 %"],
                "explain": "Les sources convergent sur 50–80 %. La cause dominante n'est pas la technique : cadrage absent, données surestimées, pas de seuil de décision.",
            },
            {
                "q": "Dans un projet IA, que spécifie-t-on à la place des règles fonctionnelles d'un cahier des charges classique ?",
                "correct": "Des objectifs mesurables et des seuils",
                "distractors": [
                    "Des maquettes d'interface détaillées",
                    "Des cas de test exhaustifs rédigés à l'avance",
                    "Des règles métier codées une par une",
                ],
                "explain": "Le livrable est un comportement appris, probabiliste : on fixe une métrique cible et des seuils d'acceptation, pas des règles déterministes.",
            },
            {
                "q": "Environ 60 % du temps d'un projet IA est consacré à quoi ?",
                "correct": "Aux données : accès, nettoyage, préparation",
                "distractors": [
                    "À l'entraînement et au réglage fin des modèles",
                    "À l'intégration dans le SI existant",
                    "À la documentation et à la conformité",
                ],
                "explain": "Environ 60 % du temps part dans les données — d'où l'exploration d'extraits réels dès le cadrage, avant d'engager le budget.",
            },
            {
                "q": "Dans CRISP-DM, quelle phase concentre 50 à 70 % de l'effort ?",
                "correct": "La préparation des données",
                "distractors": [
                    "La modélisation",
                    "L'évaluation des modèles candidats",
                    "Le déploiement en production",
                ],
                "explain": "Sélection, nettoyage, construction de variables, intégration : la préparation des données représente 50 à 70 % de l'effort du projet.",
            },
            {
                "q": "Dans un sprint d'expérimentation, conclure « l'hypothèse est fausse » est considéré comme :",
                "correct": "Un livrable valide du sprint",
                "distractors": [
                    "Un échec à re-planifier au sprint suivant",
                    "Un signal d'arrêt immédiat du projet",
                    "Un défaut de préparation du backlog",
                ],
                "explain": "Un sprint IA teste des hypothèses, pas des fonctionnalités : infirmer une hypothèse fait avancer la décision autant que la confirmer.",
            },
            {
                "q": "Quelle est l'erreur de sponsoring la plus fréquente d'un projet IA ?",
                "correct": "Un sponsor DSI par défaut, faute de porteur métier",
                "distractors": [
                    "Un sponsor trop présent dans les choix techniques",
                    "Deux sponsors métier qui se partagent l'arbitrage",
                    "Un sponsor qui exige des points d'avancement hebdomadaires",
                ],
                "explain": "Sans propriétaire métier du problème, le projet devient un exercice technique. Le sponsor porte le problème, arbitre et décide les go/no-go.",
            },
            {
                "q": "Dans l'AI Canvas, que précise le bloc « Jugement » ?",
                "correct": "Qui décide à partir de la sortie, avec quelle marge",
                "distractors": [
                    "Le niveau de risque réglementaire retenu pour le cas d'usage",
                    "La métrique d'évaluation du modèle et son seuil d'acceptation",
                    "Le volume de données d'entraînement jugé nécessaire",
                ],
                "explain": "Le système produit une prédiction ou un contenu ; le bloc Jugement dit qui décide et comment — ex. : le conseiller relit, modifie, envoie.",
            },
            {
                "q": "Matrice valeur × faisabilité : que fait-on d'un cas d'usage à valeur forte mais faisabilité faible ?",
                "correct": "On lève d'abord les freins : projet en deux temps",
                "distractors": [
                    "On le lance en premier pour crédibiliser la démarche",
                    "On l'abandonne : le ratio effort sur gain est défavorable",
                    "On le découpe en quick wins lançables immédiatement",
                ],
                "explain": "Quadrant « investir » : chantier préalable (données, conformité) avant le projet IA. Ce sont les cas valeur forte × faisabilité forte qu'on lance d'abord.",
            },
            {
                "q": "Quand l'achat d'un produit SaaS avec IA intégrée est-il le bon choix ?",
                "correct": "Cas d'usage standard, sans différenciation attendue",
                "distractors": [
                    "Dès que le budget de développement dépasse l'enveloppe prévue",
                    "Quand les données ne peuvent pas quitter l'entreprise",
                    "Quand le cas d'usage touche au cœur de métier différenciant",
                ],
                "explain": "Acheter convient aux besoins standard : rapide, maintenu, coût prévisible. Le cœur différenciant justifie de construire — et les données partent chez l'éditeur, ce qui est une limite de l'achat.",
            },
            {
                "q": "Selon l'AI Act, un système d'IA utilisé pour trier des candidatures en recrutement relève du niveau :",
                "correct": "À haut risque",
                "distractors": [
                    "À risque minimal",
                    "À risque limité",
                    "Des pratiques interdites",
                ],
                "explain": "Recrutement et évaluation des salariés sont listés à haut risque : gestion des risques, qualité des données, documentation technique, supervision humaine.",
            },
            {
                "q": "Pour un projet de ML prédictif (churn, scoring, prévision), quel est l'enjeu de pilotage principal ?",
                "correct": "La qualité des données et leur drift dans le temps",
                "distractors": [
                    "La puissance de calcul disponible pour l'entraînement",
                    "Le choix du framework de deep learning",
                    "La taille de l'équipe de data scientists",
                ],
                "explain": "Historique labellisé, volumineux, représentatif — et qui dérive : la donnée est le facteur limitant, pas le calcul ni le framework.",
            },
            {
                "q": "Comment gère-t-on l'impossibilité d'estimer le résultat d'une expérimentation ?",
                "correct": "On borne le temps investi, avec des jalons go/no-go",
                "distractors": [
                    "On ajoute une marge de 50 % aux estimations initiales",
                    "On attend d'avoir plus de données pour planifier",
                    "On confie l'estimation aux data scientists seniors",
                ],
                "explain": "Le résultat est inconnu avant d'expérimenter : on timebox l'incertitude et on force une décision aux jalons, au lieu d'estimer l'inestimable.",
            },
            {
                "q": "Quel écart constate-t-on couramment entre le coût estimé et le coût réel jusqu'à la production ?",
                "correct": "Un facteur 3",
                "distractors": ["Un facteur 1,2", "Un facteur 6", "Un facteur 10"],
                "explain": "×3 est l'ordre de grandeur courant — surtout parce que le chantier données et l'industrialisation sont sous-estimés au cadrage.",
            },
            {
                "q": "Quel est le livrable de la phase de cadrage ?",
                "correct": "La charte de projet IA",
                "distractors": [
                    "Le rapport d'expérimentation",
                    "Le jeu de données documenté et versionné",
                    "Le registre de modèles initialisé",
                ],
                "explain": "La charte (12 rubriques) clôt le cadrage. Le jeu documenté clôt la phase données, le rapport d'expérimentation le POC.",
            },
            {
                "q": "Qui définit ce qu'est une « erreur acceptable » du système ?",
                "correct": "L'expert métier",
                "distractors": [
                    "Le data scientist",
                    "Le délégué à la protection des données",
                    "L'ingénieur MLOps",
                ],
                "explain": "Il explique le processus, distingue les erreurs graves des erreurs tolérables et valide les labels — le data scientist optimise ensuite dans ce cadre.",
            },
            {
                "q": "Dans le RACI, qui est « A » (accountable) de la décision go/no-go ?",
                "correct": "Le sponsor métier",
                "distractors": [
                    "Le chef de projet / PO IA",
                    "Le data scientist référent",
                    "Le comité de direction",
                ],
                "explain": "Le sponsor décide, le PO instruit (R), les autres sont consultés. Un go/no-go sans porteur métier n'engage personne.",
            },
            {
                "q": "Au cadrage, quelle réponse disqualifie un cas d'usage ?",
                "correct": "« On veut utiliser l'IA », sans problème mesuré",
                "distractors": [
                    "« Le processus mobilise 40 ETP par an »",
                    "« Chaque erreur nous coûte environ 2 M€ par an »",
                    "« La décision est prise 5 000 fois par mois »",
                ],
                "explain": "Les trois autres réponses donnent un coût, un volume, une valeur unitaire : exactement ce qu'on cherche. La technologie sans problème est le signal d'arrêt.",
            },
            {
                "q": "Dans le TCO d'un projet IA, quel poste est le plus souvent oublié ?",
                "correct": "Le temps des experts métier (annotation, validation)",
                "distractors": [
                    "Le coût des licences logicielles de la plateforme",
                    "L'hébergement cloud de l'inférence en production",
                    "Les prestations externes d'intégration à l'existant du SI",
                ],
                "explain": "Annotation et validation mobilisent des semaines d'experts métier — un coût réel, rarement budgété, qui conditionne pourtant la qualité.",
            },
            {
                "q": "Comment chiffre-t-on un gain de productivité dans le business case ?",
                "correct": "Temps gagné × coût horaire × volume",
                "distractors": [
                    "Budget du projet × taux de marge attendu",
                    "Nombre d'utilisateurs × coût de licence évité",
                    "ETP redéployés × salaire moyen chargé",
                ],
                "explain": "La formule de base du gain de productivité ; les gains qualitatifs (satisfaction, conformité) sont explicités à part quand ils ne se chiffrent pas.",
            },
            {
                "q": "Dans la charte de projet, que fixe la rubrique « métriques et seuils » ?",
                "correct": "Métrique modèle et métrique métier, avec leurs seuils",
                "distractors": [
                    "Les seuils d'alerte du monitoring technique de production",
                    "Le budget maximal autorisé par phase du projet",
                    "Les indicateurs de vélocité de l'équipe projet",
                ],
                "explain": "Ex. : F1 ≥ 0,85 (modèle) et −30 % de temps de traitement (métier), avec la méthode d'évaluation et le jeu de test. C'est la base des go/no-go.",
            },
        ],
    },
    "m2": {
        "title": "Module 2 — Données et expérimentation (POC)",
        "questions": [
            {
                "q": "Dans le data readiness assessment, comment vérifie-t-on réellement le critère « accès » ?",
                "correct": "Un extrait réel a été obtenu et consulté",
                "distractors": [
                    "Le propriétaire des données a donné un accord de principe",
                    "Le catalogue de données mentionne la table concernée",
                    "La DSI a confirmé l'existence d'une API interne",
                ],
                "explain": "Note 4 = accès obtenu, extrait consulté : seule la consultation d'un extrait réel prouve l'accès technique et juridique. Un accord de principe n'a jamais chargé une table.",
            },
            {
                "q": "Qu'est-ce que la labellisation d'un jeu de données ?",
                "correct": "Associer à chaque exemple la réponse attendue",
                "distractors": [
                    "Chiffrer les champs sensibles avant l'entraînement",
                    "Classer les sources par niveau de confidentialité",
                    "Ajouter des métadonnées de provenance à chaque fichier",
                ],
                "explain": "Catégorie, montant, zone d'image, réponse de référence… Nécessaire à l'apprentissage supervisé et à l'évaluation de tout système, y compris génératif.",
            },
            {
                "q": "Qu'impose le principe de minimisation lors de la constitution du jeu de données ?",
                "correct": "N'extraire que les champs nécessaires au cas d'usage",
                "distractors": [
                    "Réduire le jeu de données au strict minimum statistique",
                    "Supprimer tous les champs à caractère personnel",
                    "Restreindre l'accès aux données au seul data engineer",
                ],
                "explain": "Chaque champ personnel doit être justifié par le cas d'usage. Minimiser ne veut dire ni tout supprimer, ni réduire le volume d'exemples.",
            },
            {
                "q": "À quoi sert un outil comme Great Expectations ?",
                "correct": "Exécuter des règles de qualité à chaque extraction",
                "distractors": [
                    "Versionner les jeux de données volumineux",
                    "Suivre les expérimentations et leurs métriques",
                    "Orchestrer les pipelines d'entraînement des modèles",
                ],
                "explain": "Règles déclaratives (complétude, plages, unicité, distribution) avec rapport lisible ; elles deviennent un test du pipeline en production. DVC versionne, MLflow suit, Airflow orchestre.",
            },
            {
                "q": "Quelle est la fonction première d'un POC ?",
                "correct": "Lever une incertitude identifiée et produire une décision",
                "distractors": [
                    "Démontrer la valeur du projet auprès de la direction",
                    "Livrer une première version utilisable à un panel réduit",
                    "Explorer librement les données sans objectif préalable fixé",
                ],
                "explain": "Un POC répond à une question précise (seuil atteignable ? coût tenable ?) et se termine par un go/no-go — pas par une démonstration.",
            },
            {
                "q": "Pourquoi verrouille-t-on le jeu de test dès la semaine 0, sans plus le consulter ?",
                "correct": "Pour que l'évaluation finale reste non biaisée",
                "distractors": [
                    "Pour figer le périmètre fonctionnel du projet",
                    "Pour empêcher toute fuite de données personnelles",
                    "Pour garantir la reproductibilité des entraînements",
                ],
                "explain": "Optimiser en regardant le jeu de test revient à apprendre dessus : le verdict du go/no-go ne vaut que si ce jeu n'a jamais servi pendant l'expérimentation.",
            },
            {
                "q": "Un POC affiche 85 % de réussite ; la règle métier existante fait 82 %. Que manquait-il au cadrage ?",
                "correct": "La baseline, mesurée avant d'expérimenter",
                "distractors": [
                    "Un jeu de test de taille suffisante",
                    "Une métrique adaptée au déséquilibre des classes",
                    "Un seuil de coût par requête",
                ],
                "explain": "Piège du POC sans baseline : 85 % semble bon, mais l'écart réel avec l'existant est de 3 points — à mettre en face du coût complet du projet.",
            },
            {
                "q": "Détection de fraude : rater un cas réel coûte très cher, une alerte inutile coûte peu. Quelle métrique privilégier ?",
                "correct": "Le rappel (sensibilité)",
                "distractors": [
                    "La précision",
                    "L'exactitude (accuracy)",
                    "Le taux de faux positifs",
                ],
                "explain": "Le rappel mesure la part des vrais positifs détectés. La précision se privilégie quand le faux positif coûte cher — ici c'est l'inverse.",
            },
            {
                "q": "Comment évalue-t-on un assistant RAG, faute de « bonne réponse » unique ?",
                "correct": "Sur un jeu de 100 à 300 questions construit avec le métier",
                "distractors": [
                    "En comparant ses réponses à celles d'un autre LLM en aveugle",
                    "En mesurant la satisfaction des utilisateurs après lancement",
                    "Sur la perplexité du modèle mesurée sur le corpus documentaire",
                ],
                "explain": "Questions représentatives avec réponse de référence ou critères de qualité, incluant cas difficiles et hors périmètre ; pour un RAG on juge aussi la fidélité aux sources citées.",
            },
            {
                "q": "Le « POC purgatoire » — un POC qui « marche presque » depuis six mois — a pour cause :",
                "correct": "L'absence de timebox et de seuil de décision",
                "distractors": [
                    "Un jeu de test trop difficile pour le modèle",
                    "Une équipe sous-dimensionnée en data engineers",
                    "Un sponsor trop pressé de passer en production",
                ],
                "explain": "Remède : critères écrits dès la semaine 0, jalons intermédiaires (S2, S4), décision forcée à date fixe.",
            },
            {
                "q": "Que mesure l'accord inter-annotateurs pendant la labellisation ?",
                "correct": "La cohérence des labels entre annotateurs",
                "distractors": [
                    "La vitesse moyenne d'annotation par exemple",
                    "La couverture du périmètre par le jeu labellisé",
                    "Le taux d'exemples rejetés comme ambigus",
                ],
                "explain": "Un accord faible signale une consigne floue ou une tâche mal définie : les labels seront bruités, et le modèle apprendra ce bruit.",
            },
            {
                "q": "Quelle place pour les données synthétiques dans le sourcing ?",
                "correct": "Un complément, à manier avec prudence",
                "distractors": [
                    "Un substitut complet aux données réelles",
                    "Une exigence du RGPD pour l'entraînement",
                    "Un moyen d'éviter la labellisation manuelle",
                ],
                "explain": "Elles complètent des cas rares ou sensibles, mais reproduisent les biais de leur générateur et ne remplacent pas la réalité du terrain.",
            },
            {
                "q": "Comment organise-t-on les accès aux données du projet ?",
                "correct": "Environnements séparés et comptes nominatifs",
                "distractors": [
                    "Un compte de service partagé par l'équipe data",
                    "Un accès complet limité à la durée du POC",
                    "Une copie locale chez chaque data scientist",
                ],
                "explain": "Exploration, entraînement et production sont séparés ; comptes nominatifs et journalisation. Le propriétaire des données autorise, le data engineer met en place.",
            },
            {
                "q": "À quoi servent DVC ou LakeFS ?",
                "correct": "Versionner les jeux de données",
                "distractors": [
                    "Profiler la qualité des données",
                    "Annoter les exemples d'entraînement",
                    "Fédérer les accès aux bases sources",
                ],
                "explain": "Retrouver exactement les données d'un entraînement passé : indispensable pour reproduire un modèle ou auditer un résultat.",
            },
            {
                "q": "Une hypothèse d'expérimentation bien formulée contient :",
                "correct": "Un test, un critère chiffré, une durée max",
                "distractors": [
                    "Une intuition à explorer sans limite de temps",
                    "Un objectif de performance de long terme",
                    "La liste des modèles à essayer successivement",
                ],
                "explain": "Ex. : « le gradient boosting dépasse F1 0,75 — test sur le jeu de validation — 4 jours max ». Sans critère ni durée, l'hypothèse devient un POC purgatoire miniature.",
            },
            {
                "q": "Au jalon S2, une approche simple ne dépasse pas la baseline. Que suspecter d'abord ?",
                "correct": "Les données, avant l'algorithme",
                "distractors": [
                    "Un réglage insuffisant des hyperparamètres",
                    "Une baseline mesurée trop haute",
                    "Un jeu de test trop petit pour conclure",
                ],
                "explain": "Si une approche simple ne bat pas la baseline, le signal n'est probablement pas dans les données fournies — complexifier le modèle n'y changera rien.",
            },
            {
                "q": "Pourquoi préférer le F1 à l'exactitude sur des classes déséquilibrées ?",
                "correct": "Prédire toujours la majorité donne déjà une exactitude élevée",
                "distractors": [
                    "Le F1 pondère chaque classe par sa fréquence relative dans le jeu",
                    "Le F1 est plus simple à expliquer au métier",
                    "L'exactitude ne se calcule pas sur plus de deux classes",
                ],
                "explain": "Avec 95 % de négatifs, prédire « négatif » partout donne 95 % d'exactitude et 0 détection. Le F1 combine précision et rappel et révèle ce vide.",
            },
            {
                "q": "Le « POC vitrine » impressionne en démo mais déçoit ensuite. Sa cause :",
                "correct": "Un jeu de test non représentatif des cas réels",
                "distractors": [
                    "Un modèle trop simple pour la complexité du problème",
                    "Une baseline jamais mesurée au moment du cadrage",
                    "Un sponsor absent des démonstrations intermédiaires",
                ],
                "explain": "La démo tourne sur des exemples choisis. Remède : évaluation sur jeu verrouillé incluant les cas difficiles, ambigus et hors périmètre.",
            },
            {
                "q": "Pour un RAG, quel critère s'ajoute à l'exactitude des réponses ?",
                "correct": "La fidélité aux sources citées",
                "distractors": [
                    "La vitesse d'indexation du corpus",
                    "La taille du modèle d'embedding",
                    "Le nombre de documents ingérés",
                ],
                "explain": "Une réponse exacte mais non appuyée sur les sources citées reste un risque : l'utilisateur ne peut pas vérifier, la confiance ne se construit pas.",
            },
            {
                "q": "À partir de quand utiliser un outil de suivi d'expérimentations (MLflow, W&B…) ?",
                "correct": "Dès la première expérience",
                "distractors": [
                    "À partir du passage en production",
                    "Quand l'équipe dépasse trois personnes",
                    "Au moment du rapport final du POC",
                ],
                "explain": "Paramètres, métriques, versions du code et des données : la comparaison et la reproductibilité exigent l'historique complet, pas ses trois dernières lignes.",
            },
        ],
    },
    "m3": {
        "title": "Module 3 — Industrialiser : MLOps et sécurité",
        "questions": [
            {
                "q": "En fin de POC, le modèle est « un fichier sur un poste ». Qu'exige la production ?",
                "correct": "Un registre de modèles : version, métadonnées, approbation",
                "distractors": [
                    "Une sauvegarde chiffrée du fichier sur le serveur de production",
                    "Un dépôt Git contenant le notebook d'entraînement final",
                    "Une copie du modèle chez chaque membre de l'équipe technique",
                ],
                "explain": "Le registre trace quelle version tourne, avec quelles données et quelle approbation — condition du déploiement automatisé et du retour arrière.",
            },
            {
                "q": "Que désigne le « CT » qui s'ajoute au CI/CD dans MLOps ?",
                "correct": "L'entraînement continu, déclenché par drift ou calendrier",
                "distractors": [
                    "Les tests continus exécutés à chaque commit du code",
                    "La certification technique du modèle avant chaque déploiement",
                    "Le contrôle de trafic lors des déploiements progressifs",
                ],
                "explain": "Continuous Training : réentraîner automatiquement (nouvelles données, drift détecté, planification) — la boucle propre aux systèmes IA. Les tests à chaque commit relèvent de la CI.",
            },
            {
                "q": "Quel niveau de test est spécifique aux systèmes IA, en plus des tests logiciels classiques ?",
                "correct": "Les tests de données : schéma, plages, distribution",
                "distractors": [
                    "Les tests unitaires des fonctions de l'API",
                    "Les tests d'intégration entre services applicatifs",
                    "Les tests de charge sur l'environnement de pré-production",
                ],
                "explain": "On teste aussi les données (schéma, complétude, dérive, absence de fuite) et le modèle (performance vs seuil, non-régression) — pas seulement le code.",
            },
            {
                "q": "Une instruction cachée dans un document fourni au modèle détourne son comportement. C'est :",
                "correct": "Une injection de prompt",
                "distractors": [
                    "Un empoisonnement de données",
                    "Une fuite d'information",
                    "Une extraction de modèle",
                ],
                "explain": "L'injection agit à l'inférence, via les entrées. L'empoisonnement corrompt l'entraînement ; la fuite révèle des données ; l'extraction reconstruit le modèle par requêtes massives.",
            },
            {
                "q": "Quelle parade réduit l'impact d'une injection de prompt réussie ?",
                "correct": "Le moindre privilège des outils du modèle",
                "distractors": [
                    "Le chiffrement de bout en bout des conversations",
                    "Un prompt système plus long et plus détaillé",
                    "La journalisation exhaustive des requêtes",
                ],
                "explain": "Si l'injection passe, un modèle aux droits minimaux ne peut pas faire grand-chose. Un prompt système détaillé n'est pas une barrière fiable ; la journalisation détecte, elle ne limite pas.",
            },
            {
                "q": "En production, comment détecte-t-on le drift des données d'entrée ?",
                "correct": "En comparant leur distribution à l'entraînement (PSI, KS)",
                "distractors": [
                    "En suivant le taux d'erreurs HTTP de l'API de prédiction",
                    "En re-labellisant chaque semaine un échantillon des prédictions",
                    "En surveillant la consommation mémoire des serveurs",
                ],
                "explain": "Alerte typique : PSI > 0,2 sur une variable clé. La re-labellisation mesure la qualité réelle — utile mais plus lente et coûteuse ; les erreurs HTTP relèvent de la santé technique.",
            },
            {
                "q": "Le taux de prédictions positives double en une semaine, sans changement du code. Quelle famille d'alerte ?",
                "correct": "Drift des prédictions",
                "distractors": [
                    "Drift des données d'entrée",
                    "Santé technique",
                    "Qualité métier",
                ],
                "explain": "Quatre familles : santé technique, drift des données (entrées), drift des prédictions (sorties), qualité métier. Un taux de positifs qui double est un signal de sortie — il déclenche ensuite l'analyse des entrées.",
            },
            {
                "q": "Que mesure la latence P95 d'un service de prédiction ?",
                "correct": "Le temps sous lequel 95 % des requêtes sont servies",
                "distractors": [
                    "Le temps moyen de réponse calculé sur 95 jours glissants",
                    "La latence moyenne des 95 requêtes les plus rapides",
                    "Le pourcentage de requêtes servies sans erreur",
                ],
                "explain": "Percentile 95 : 5 % des requêtes dépassent cette durée. Plus parlant que la moyenne, qui masque les pics ressentis par les utilisateurs.",
            },
            {
                "q": "Quel outil open source couvre le suivi d'expérimentations et le registre de modèles ?",
                "correct": "MLflow",
                "distractors": ["Kubeflow", "Airflow", "Great Expectations"],
                "explain": "MLflow enregistre paramètres, métriques et artefacts, et gère le registre. Kubeflow orchestre des pipelines sur Kubernetes, Airflow des workflows, Great Expectations valide la qualité des données.",
            },
            {
                "q": "Pourquoi exige-t-on un pipeline de préparation « code, pas de manipulations manuelles » ?",
                "correct": "Pour être rejouable et audité à l'identique",
                "distractors": [
                    "Pour réduire le coût de calcul des transformations",
                    "Pour satisfaire aux exigences du RGPD",
                    "Pour accélérer l'entraînement des modèles",
                ],
                "explain": "Reproductibilité : mêmes entrées, mêmes sorties, le tout versionné et journalisé. Une manipulation manuelle casse la traçabilité et interdit le rejeu.",
            },
            {
                "q": "Quand un feature store se justifie-t-il ?",
                "correct": "Quand des variables sont partagées entre modèles",
                "distractors": [
                    "Dès qu'un modèle dépasse une dizaine de variables",
                    "Quand le volume de données dépasse le téraoctet",
                    "Quand l'équipe utilise plusieurs langages de programmation",
                ],
                "explain": "Il évite de recalculer (et de diverger) les mêmes variables entre entraînement et production, et entre équipes. Un seul modèle isolé s'en passe.",
            },
            {
                "q": "Qu'est-ce qu'un déploiement « shadow » d'un modèle ?",
                "correct": "Le modèle tourne en parallèle, sans effet sur les décisions",
                "distractors": [
                    "Le modèle est exposé à une petite fraction des utilisateurs",
                    "Le modèle est activé la nuit, hors des heures ouvrées",
                    "Le modèle remplace l'ancien, avec retour arrière possible",
                ],
                "explain": "Ses sorties sont comparées au réel sans agir. L'exposition d'une fraction du trafic, c'est le canary — l'étape suivante.",
            },
            {
                "q": "Qu'est-ce que l'empoisonnement de données ?",
                "correct": "Des exemples corrompus glissés dans l'entraînement",
                "distractors": [
                    "Une instruction cachée dans une entrée à l'inférence",
                    "Le vol du jeu d'entraînement par un tiers malveillant",
                    "Une dérive progressive des données sources en production",
                ],
                "explain": "L'empoisonnement vise l'apprentissage ; l'instruction cachée à l'inférence est l'injection de prompt ; la dérive naturelle est le drift.",
            },
            {
                "q": "Avant de promouvoir un nouveau modèle, que vérifie le test de non-régression ?",
                "correct": "Ses résultats sur un jeu de référence, face à l'ancien",
                "distractors": [
                    "La stabilité de l'API sous montée en charge progressive",
                    "L'absence de vulnérabilités dans les dépendances",
                    "La conformité du code aux conventions de l'équipe",
                ],
                "explain": "Même jeu de référence, mêmes métriques : le nouveau modèle doit tenir le seuil et ne pas régresser sur les cas que l'ancien traitait bien.",
            },
            {
                "q": "Comment mesure-t-on la qualité métier réelle d'un modèle en production ?",
                "correct": "Un échantillon de sorties re-labellisé régulièrement",
                "distractors": [
                    "Le score du modèle mesuré sur son jeu d'entraînement",
                    "La latence P95 et le taux d'erreurs HTTP de l'API",
                    "Le taux de disponibilité mensuel du service",
                ],
                "explain": "Seule une vérité terrain fraîche (re-labellisation, retours utilisateurs) dit si le modèle reste bon. Latence et disponibilité relèvent de la santé technique.",
            },
            {
                "q": "Que permet le versionnage conjoint du modèle et de ses données d'entraînement ?",
                "correct": "Reproduire ou annuler un déploiement à l'identique",
                "distractors": [
                    "Réduire la taille de stockage des artefacts produits",
                    "Accélérer l'entraînement des versions suivantes",
                    "Se passer de tests avant les déploiements mineurs",
                ],
                "explain": "Rejouer un entraînement, auditer un résultat, revenir à la version précédente : sans les deux versions liées, le retour arrière est approximatif.",
            },
            {
                "q": "Quelle validation ajoute-t-on en sortie d'un LLM avant d'agir ?",
                "correct": "Un contrôle du format et du contenu de la sortie",
                "distractors": [
                    "Une signature numérique apposée sur la réponse",
                    "Une relecture systématique par le data scientist",
                    "Un archivage brut de la réponse générée",
                ],
                "explain": "Schéma attendu, valeurs plausibles, absence de contenu interdit : la sortie d'un modèle probabiliste se valide avant de déclencher une action.",
            },
            {
                "q": "Que déclenche un commit dans la CI d'un projet IA, en plus des tests logiciels ?",
                "correct": "Les tests de schéma et de qualité des données",
                "distractors": [
                    "Le réentraînement complet du modèle en production",
                    "La promotion automatique dans le registre de modèles",
                    "Le déploiement immédiat en pré-production",
                ],
                "explain": "CI = tests code + données à chaque modification. Le réentraînement relève du CT, le déploiement du CD — chacun avec ses déclencheurs propres.",
            },
            {
                "q": "Quel est le rôle d'un orchestrateur (Airflow, Kubeflow Pipelines) ?",
                "correct": "Enchaîner et planifier les étapes du pipeline",
                "distractors": [
                    "Répartir la charge des requêtes d'inférence",
                    "Stocker les artefacts des expérimentations",
                    "Surveiller la dérive des données en production",
                ],
                "explain": "Ingestion, préparation, entraînement, évaluation : l'orchestrateur exécute la chaîne, la rejoue et journalise — la répartition de charge relève du serving.",
            },
            {
                "q": "« P95 > 1 s » et « taux d'erreur > 1 % » sont des alertes de :",
                "correct": "Santé technique",
                "distractors": [
                    "Drift des prédictions",
                    "Qualité métier",
                    "Drift des données d'entrée",
                ],
                "explain": "Latence, erreurs, disponibilité, débit : la famille santé technique — nécessaire mais aveugle à la qualité des prédictions elles-mêmes.",
            },
        ],
    },
    "m4": {
        "title": "Module 4 — Piloter, déployer, exploiter",
        "questions": [
            {
                "q": "Que faut-il, entre autres, pour franchir le jalon J1 « données prêtes » ?",
                "correct": "Readiness ≥ 3, jeu de test verrouillé, baseline mesurée",
                "distractors": [
                    "Le modèle candidat entraîné et son rapport d'expérimentation",
                    "L'architecture de production validée par l'équipe sécurité",
                    "Le pilote utilisateur planifié avec le management",
                ],
                "explain": "J1 clôt la phase données. Le rapport d'expérimentation relève de J2 (go/no-go POC), l'architecture validée de J3, le pilote de J4.",
            },
            {
                "q": "Dans le backlog, comment estime-t-on une « hypothèse » d'expérimentation ?",
                "correct": "Par une durée maximale, pas en points d'effort",
                "distractors": [
                    "En points de story, comme les autres tickets",
                    "Par le nombre d'expériences MLflow associées",
                    "Par la valeur métier attendue, chiffrée en euros",
                ],
                "explain": "On ne sait pas combien de temps il faut pour « trouver » : on borne le temps investi (timebox), et « infirmée » est un résultat valide.",
            },
            {
                "q": "Quelle règle s'applique aux décisions d'un comité go/no-go ?",
                "correct": "Une décision explicite parmi les options prévues",
                "distractors": [
                    "Un consensus unanime de toutes les parties prenantes",
                    "Un vote à la majorité qualifiée des membres présents",
                    "Un avis consultatif transmis au comité de direction",
                ],
                "explain": "Go, no-go, pivot ou itération bornée — sur la base des critères écrits. Jamais de « on continue pour voir ».",
            },
            {
                "q": "À quoi sert une model card ?",
                "correct": "Documenter usages, performances et limites du modèle",
                "distractors": [
                    "Tracer les hyperparamètres de chaque run d'entraînement",
                    "Décrire l'origine et la composition du jeu de données",
                    "Certifier la conformité RGPD du traitement mis en œuvre",
                ],
                "explain": "La model card s'adresse à l'équipe, à l'audit et au métier. La datasheet documente les données ; le suivi d'expérimentations trace les runs.",
            },
            {
                "q": "Quelle clause conditionne la conformité RGPD lors de l'usage d'une API de modèle ?",
                "correct": "L'usage et la conservation de nos données par l'éditeur",
                "distractors": [
                    "Le préavis contractuel en cas de dépréciation d'un modèle",
                    "La disponibilité garantie par le SLA du service",
                    "La réversibilité prévue en fin de contrat",
                ],
                "explain": "Nos données servent-elles à entraîner leurs modèles ? Sont-elles conservées, où, par quels sous-traitants ? Les autres clauses comptent, mais celle-ci est éliminatoire.",
            },
            {
                "q": "Pour un système d'IA générative en production, quel poste de coût domine et varie avec l'usage ?",
                "correct": "L'inférence : requêtes × longueur des contextes",
                "distractors": [
                    "La maintenance corrective de l'application et des connecteurs",
                    "Le stockage des journaux de conversation",
                    "Les licences de la plateforme MLOps retenue",
                ],
                "explain": "Un RAG envoie des documents entiers en contexte : le coût suit le volume d'appels et la taille des contextes — d'où un suivi FinOps par cas d'usage.",
            },
            {
                "q": "Quelle charge de maintenance prévoir en run pour un système IA ?",
                "correct": "20 à 40 % d'un ETP par système",
                "distractors": [
                    "Moins de 5 % d'un ETP par système",
                    "Un ETP complet dédié par système",
                    "Aucune : le réentraînement est automatisé",
                ],
                "explain": "Surveillance, réentraînement, support : 20 à 40 % d'un ETP. La CI/CD/CT automatise le chemin, pas la vigilance ni les arbitrages.",
            },
            {
                "q": "Quel critère d'usage valide le bilan d'un pilote (jalon J4) ?",
                "correct": "Au moins 60 % des pilotes utilisent le système",
                "distractors": [
                    "Au moins 90 % des pilotes se sont connectés une fois",
                    "La totalité des utilisateurs formés au dispositif",
                    "Un NPS supérieur à 50 mesuré sur le panel du pilote",
                ],
                "explain": "Usage réel ≥ 60 %, métrique métier confrontée au business case, incidents traités : c'est l'usage régulier qui compte, pas la connexion unique.",
            },
            {
                "q": "Au registre des risques, quelle réponse au risque « données insuffisantes ou inaccessibles » ?",
                "correct": "Exploration d'extraits réels dès le cadrage",
                "distractors": [
                    "Achat de données synthétiques en compensation",
                    "Report du sujet à la phase d'expérimentation",
                    "Doublement du budget de la phase données",
                ],
                "explain": "Le risque le plus fréquent se traite en préventif : extraits réels au cadrage, chantier données préalable, ou abandon avant d'avoir dépensé. Le synthétique se manie avec prudence, en complément.",
            },
            {
                "q": "« Faire un projet d'IA générative » sans problème métier identifié : quelle parade ?",
                "correct": "La phrase de cas d'usage et l'AI Canvas avant tout",
                "distractors": [
                    "Un hackathon interne pour faire émerger des idées",
                    "Une veille technologique structurée sur les LLM",
                    "Un appel d'offres pour comparer les solutions du marché",
                ],
                "explain": "L'IA est un moyen : le projet démarre par un problème mesuré aujourd'hui (coût, délai, erreurs), pas par une technologie à caser.",
            },
            {
                "q": "Quel format de reporting pour le sponsor ?",
                "correct": "Un tableau de bord d'une page, 30 minutes par mois",
                "distractors": [
                    "Une synthèse de deux pages chaque trimestre",
                    "Un rapport détaillé à chaque fin de sprint",
                    "Un point hebdomadaire d'une heure en visioconférence",
                ],
                "explain": "Jalons, valeur, risques, décisions à prendre — mensuel. La synthèse trimestrielle de deux pages s'adresse à la direction et au comité IA.",
            },
            {
                "q": "Quel document décrit l'origine, la composition et les limites du jeu de données ?",
                "correct": "La datasheet (fiche de données)",
                "distractors": [
                    "La model card du modèle",
                    "La charte de projet IA",
                    "Le rapport d'expérimentation du POC",
                ],
                "explain": "Origine, collecte, prétraitements, usages prévus et déconseillés, conformité — mise à jour à chaque réentraînement. La model card documente le modèle.",
            },
            {
                "q": "Risque « seuil de performance non atteint » : quel signal précoce au registre des risques ?",
                "correct": "Un écart > 20 % au jalon S2 ou S4",
                "distractors": [
                    "Le turnover dans l'équipe de data science",
                    "Le dépassement du budget de la phase de cadrage",
                    "Le retard de signature de la charte de projet",
                ],
                "explain": "Les jalons intermédiaires du POC servent de capteurs : un écart de plus de 20 % au seuil déclenche la réponse prévue (périmètre réduit, itération bornée, arrêt).",
            },
            {
                "q": "Que veut savoir le métier (utilisateurs, experts) dans la communication projet ?",
                "correct": "Ce que ça change pour eux, et quand",
                "distractors": [
                    "Le détail des hyperparamètres retenus",
                    "La consommation budgétaire par phase",
                    "L'architecture technique de la solution",
                ],
                "explain": "Résultats sur leurs cas concrets, calendrier, ce qui est attendu d'eux. Le budget intéresse le sponsor, l'architecture les équipes techniques.",
            },
            {
                "q": "Pourquoi le coût par requête d'un RAG est-il élevé ?",
                "correct": "Chaque requête embarque des documents entiers en contexte",
                "distractors": [
                    "L'index vectoriel complet est recalculé à chaque question posée",
                    "Les embeddings du corpus sont refacturés à chaque appel",
                    "Le modèle est réentraîné après chaque session utilisateur",
                ],
                "explain": "Le coût d'inférence suit la longueur des contextes : les passages récupérés partent dans chaque appel. L'indexation, elle, est faite une fois puis mise à jour.",
            },
            {
                "q": "Dans quel ordre déploie-t-on progressivement pendant le pilote ?",
                "correct": "Shadow d'abord, puis canary",
                "distractors": [
                    "Canary d'abord, puis shadow",
                    "Bascule complète, puis observation",
                    "A/B test permanent sur toute la base",
                ],
                "explain": "On observe sans agir (shadow), puis on expose une fraction réelle du trafic (canary), avant d'élargir — chaque étape peut arrêter la suivante.",
            },
            {
                "q": "Quels types de tickets ajoute-t-on au backlog d'un projet IA ?",
                "correct": "« Hypothèse » et « chantier données »",
                "distractors": [
                    "« Incident modèle » et « astreinte IA »",
                    "« Dette technique » et « spike d'architecture »",
                    "« Étude préalable » et « prototype jetable »",
                ],
                "explain": "À côté des story, tâche et bug : l'hypothèse (avec critère et durée max) et le chantier données, les deux natures de travail propres à l'IA.",
            },
            {
                "q": "Pourquoi exiger un préavis de dépréciation dans le contrat d'une API de modèle ?",
                "correct": "Le retrait d'un modèle impose de re-tester tout le système",
                "distractors": [
                    "La facturation change à chaque nouvelle version publiée",
                    "Le support cesse d'être assuré sur les anciennes clés d'API",
                    "Les quotas d'appels sont remis à zéro à chaque version",
                ],
                "explain": "Un modèle remplacé ne se comporte pas à l'identique : prompts, évaluations et seuils sont à rejouer. Sans préavis, cette charge tombe sans prévenir.",
            },
            {
                "q": "Qu'est-ce qu'une « feature » (variable) d'un modèle ?",
                "correct": "Une donnée d'entrée du modèle",
                "distractors": [
                    "Une fonctionnalité livrée de l'application",
                    "Un paramètre interne appris par le modèle",
                    "Une métrique de suivi de la performance",
                ],
                "explain": "Les features alimentent le modèle ; les paramètres appris (poids) en sont le résultat. Le feature engineering consiste à construire ces variables.",
            },
            {
                "q": "Par quoi commence le plan d'action, dès la première semaine ?",
                "correct": "Phrase de cas d'usage, sponsor, extrait réel demandé",
                "distractors": [
                    "Choix de la plateforme MLOps et du fournisseur cloud",
                    "Recrutement d'un data scientist senior en interne",
                    "Rédaction du dossier de conformité AI Act complet",
                ],
                "explain": "Un problème formulé, un porteur, des données vues en vrai : tout le reste (outillage, équipe, conformité détaillée) découle de ces trois preuves.",
            },
        ],
    },
}


def _shuffle_options(correct, distractors, slot, rng):
    """Place `correct` a la position `slot` (0..3), melange les distracteurs."""
    d = distractors[:]
    rng.shuffle(d)
    opts = []
    di = 0
    for i in range(4):
        if i == slot:
            opts.append(correct)
        else:
            opts.append(d[di])
            di += 1
    return opts


def build_quizzes():
    """Construit les quiz avec options ordonnees (deterministe) + index de la bonne reponse."""
    out = {}
    for qid, mod in RAW.items():
        rng = random.Random("gp-seed-" + qid)  # deterministe et stable
        questions = []
        for i, item in enumerate(mod["questions"]):
            slot = PLACEMENT[i % len(PLACEMENT)]
            opts = _shuffle_options(item["correct"], item["distractors"], slot, rng)
            questions.append(
                {
                    "q": item["q"],
                    "options": opts,
                    "answer": opts.index(item["correct"]),
                    "explain": item["explain"],
                }
            )
        out[qid] = {"id": qid, "title": mod["title"], "questions": questions}
    return out


QUIZZES = build_quizzes()
QUIZ_ORDER = ["m1", "m2", "m3", "m4"]
