# DYNASTY — téléchargements Windows

Distributions de test du prototype **DYNASTY: A Century of Power**.

[Téléchargements et instructions](https://github.com/SachaRM7/DYNASTY-Releases/releases)

- **Portable** : ouvrir le fichier `.exe`, sans installation ; remplacer le fichier pour changer de version.
- **Installer** : installation pour l'utilisateur courant, avec raccourci dans le menu Démarrer ; lancer la nouvelle version de l'installateur pour mettre à niveau.

Les deux versions partagent le profil `%APPDATA%\DYNASTY-Prototype` et l'origine `dynasty://game/`. Avant de changer de version, exporter la partie en JSON depuis **Sauvegardes et réglages**. Ne pas supprimer ce profil.

Les exécutables J4 0.5.0 sont des versions de test **non signées**, avec des mises à jour **manuelles**. Les sommes SHA-256 vérifient l'intégrité des fichiers ; elles ne remplacent pas une signature d'éditeur. Aucun compte GitHub, Node.js ou terminal n'est nécessaire pour jouer.

J4 ajoute des engagements de travail, personnels et de repos, des arbitrages entre obligations et des communications situées. Un personnage occupé peut différer un rendez-vous ; une consigne attend son destinataire au fournil, puis sa réponse est portée à pied. La réception d'une réponse dépend d'une rencontre réelle. Une absence de nouvelles ne prouve pas l'échec.

Les ressources du HUD J3.5 sont conservées : Argent, Capacité organisationnelle, Lignée et Notoriété en haut ; stocks de pain, farine et bois dans la boulangerie. Les trois indicateurs futurs affichent — sans statistique inventée. Argent et caisse représentent temporairement le même solde. Les relevés de stocks restent datés en cas d'absence.

Le soutien délégué J3 et la simulation J1/J2 sont conservés. Le jeu propose les mandats individuels, le transport réel du pain, les refus, retards et livraisons partielles, ainsi que les comptes rendus localisés. Organisation, Ville et Pays restent à venir. Les paramètres du laboratoire restent expérimentaux.

Pour essayer : Relations → Collectif et contacts → Soutien délégué. Rencontrer Jules au fournil, proposer un mandat, puis préparer une livraison. Vous pouvez y laisser une consigne pendant la validité du mandat, annoncer le lieu de réponse et vous y rendre. Une mission acceptée n'est pas encore livrée ; les nouvelles dépendent de votre présence et des comptes rendus.

Le format de sauvegarde est **v5**, avec lecture de v1/v2/v3/v4/v5. Passer de 0.4.1 à 0.5.0 conserve les parties et les missions J3 en cours ; les agendas et communications sont ajoutés sans remise à zéro. Les clés des anciennes sauvegardes sont conservées. Les applications antérieures ne savent pas ouvrir une v5 : conserver un export antérieur pour un retour de version. Fermer le jeu avant de remplacer le Portable ou de lancer le nouvel Installer ; ne pas désinstaller ni supprimer le profil. Le navigateur conserve un stockage séparé : utiliser l'export/import JSON pour transférer une partie.

Les releases 0.4.0 et 0.4.1 restent disponibles. Les deux distributions 0.5.0 partagent le même profil et le format v5. Les fichiers publiés correspondent aux fichiers exécutés sous Windows, sans reconstruction lors de la publication ; `verification.json` identifie le commit et les empreintes. Les paramètres sont expérimentaux : carte SVG, un collectif et laboratoire de 30 jours, pas encore le jeu commercial complet.

- [Portable Windows x64](https://github.com/SachaRM7/DYNASTY-Releases/releases/download/v0.5.0/DYNASTY-0.5.0-Windows-x64.exe)
- [Installer Windows x64](https://github.com/SachaRM7/DYNASTY-Releases/releases/download/v0.5.0/DYNASTY-Setup-0.5.0-x64.exe)
- [Archives ZIP, instructions et SHA-256](https://github.com/SachaRM7/DYNASTY-Releases/releases/tag/v0.5.0)

Ce dépôt public est réservé aux distributions. Le dépôt de développement reste privé.

[Version navigateur jouable](https://dynasty-test-rouge.vercel.app)
