# DYNASTY — téléchargements Windows

Distributions de test du prototype **DYNASTY: A Century of Power**.

[Téléchargements et instructions](https://github.com/SachaRM7/DYNASTY-Releases/releases)

- **Portable** : ouvrir le fichier `.exe`, sans installation ; remplacer le fichier pour changer de version.
- **Installer** : installation pour l'utilisateur courant, avec raccourci dans le menu Démarrer ; lancer la nouvelle version de l'installateur pour mettre à niveau.

Les deux versions partagent le profil `%APPDATA%\DYNASTY-Prototype` et l'origine `dynasty://game/`. Avant de changer de version, exporter la partie en JSON depuis **Sauvegardes et réglages**. Ne pas supprimer ce profil.

Les exécutables J3.5 0.4.1 sont des versions de test **non signées**. Les mises à jour automatiques restent désactivées jusqu'à la configuration de la signature Windows et à la validation d'une mise à jour réelle. Les sommes SHA-256 permettent de vérifier l'intégrité des téléchargements.

J3.5 corrige les couches de ressources du HUD : Argent, Capacité organisationnelle, Lignée et Notoriété en haut ; stocks de pain, farine et bois dans la boulangerie. Les trois indicateurs futurs affichent — sans statistique inventée. Argent et caisse représentent temporairement le même solde. Les relevés de stocks restent datés en cas d’absence.

Le soutien délégué J3 et la simulation J1/J2 sont conservés. Le jeu propose les mandats individuels, le transport réel du pain, les refus, retards et livraisons partielles, ainsi que les comptes rendus localisés. Organisation, Ville et Pays restent à venir. Les paramètres du laboratoire restent expérimentaux.

Pour essayer la délégation : Relations → Collectif et contacts → Soutien délégué. Rencontrer Jules au fournil, proposer un mandat, puis préparer une livraison. Une mission acceptée n’est pas encore livrée ; les nouvelles dépendent de votre présence et des comptes rendus.

Le format de sauvegarde reste v4, identique à 0.4.0. Passer de 0.4.0 à 0.4.1 conserve les parties, y compris les missions en cours. Les sauvegardes v1/v2/v3 sont migrées en v4 sans remise à zéro. La version précédente 0.3.2 ne sait pas ouvrir une v4 : conserver votre export antérieur si vous souhaitez revenir à cette ancienne version. Fermer le jeu avant de remplacer le Portable ou de lancer le nouvel Installer ; ne pas désinstaller ni supprimer le profil.

La release 0.4.0 est conservée. Les deux distributions 0.4.1 fonctionnent avec le même profil et le même format v4.

Ce dépôt public est réservé aux distributions. Le dépôt de développement reste privé.

[Version navigateur jouable](https://dynasty-test-rouge.vercel.app)
