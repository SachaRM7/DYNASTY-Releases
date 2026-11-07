# DYNASTY — téléchargements Windows

Distributions de test du prototype **DYNASTY: A Century of Power**.

[Téléchargements et instructions](https://github.com/SachaRM7/DYNASTY-Releases/releases)

- **Portable** : ouvrir le fichier `.exe`, sans installation ; remplacer le fichier pour changer de version.
- **Installer** : installation pour l'utilisateur courant, avec raccourci dans le menu Démarrer ; lancer la nouvelle version de l'installateur pour mettre à niveau.

Les deux versions partagent le profil `%APPDATA%\DYNASTY-Prototype` et l'origine `dynasty://game/`. Avant de changer de version, exporter la partie en JSON depuis **Sauvegardes et réglages**. Ne pas supprimer ce profil.

Les exécutables sont des versions de test **non signées**. Les mises à jour automatiques restent désactivées jusqu'à la configuration de la signature Windows et à la validation d'une mise à jour réelle. Les sommes SHA-256 permettent de vérifier l'intégrité des téléchargements.

Ce dépôt public est réservé aux distributions. Le dépôt de développement reste privé.

[Version navigateur jouable](https://dynasty-test-rouge.vercel.app)

La campagne Proto 2 **0.6.2** est jouable dans le navigateur. Son candidat Windows
est préparé dans la branche `work/proto2-distribution` ; **aucun exécutable 0.6.x
n’est publié tant que les tests Windows ne passent pas**. GitHub Actions signale
actuellement un verrouillage du compte pour facturation. Les exécutables vérifiés
restent ceux de **0.5.0**. Le bundle de validation contient seulement le jeu compilé,
l’enveloppe Electron et les tests de distribution ; aucune référence privée du créateur.
