# DYNASTY — téléchargements Windows

Distributions de test de **DYNASTY: A Century of Power**, Windows 10/11 x64.

## Version 0.6.3

- [Portable, sans installation](https://github.com/SachaRM7/DYNASTY-Releases/releases/download/v0.6.3/DYNASTY-0.6.3-Windows-x64.exe)
- [Installer, raccourci dans le menu Démarrer](https://github.com/SachaRM7/DYNASTY-Releases/releases/download/v0.6.3/DYNASTY-Setup-0.6.3-x64.exe)
- [Archives ZIP, instructions et empreintes SHA-256](https://github.com/SachaRM7/DYNASTY-Releases/releases/tag/v0.6.3)

Aucun compte GitHub, Node.js ou terminal n'est nécessaire pour jouer. Cette version
conserve le Proto 2 (1850), accessible par « Explorer le Proto 2 · trois quartiers »,
et le laboratoire historique J1–J4 (1852). Les paramètres de simulation restent
expérimentaux ; ce n'est pas le jeu commercial complet.

## Mises à jour

Ouvrir **Sauvegardes et réglages → Mises à jour**.

- Désactivées : le jeu vérifie uniquement sur demande, puis propose le téléchargement.
- Activées : il recherche au lancement et toutes les six heures, puis télécharge en arrière-plan.
- Une installation exige une confirmation et une sauvegarde réussie. Elle n'interrompt
  pas une partie à l'improviste. Le Portable conserve son nom et son dossier.

Les anciennes versions sans cet updater doivent être mises à niveau **une première
fois manuellement**. Fermer DYNASTY, puis remplacer le Portable ou lancer le nouvel
Installer, sans désinstallation préalable.

Les exécutables n'ont pas de certificat d'éditeur Windows Authenticode. Windows peut
afficher un avertissement. Les métadonnées de mise à jour sont signées Ed25519 et
les fichiers téléchargés sont vérifiés avant installation. Aucun certificat payant
ni abonnement n'est nécessaire à ce fonctionnement.

## Conserver ses parties

Les deux distributions partagent `%APPDATA%\DYNASTY-Prototype` et l'origine
`dynasty://game/`. Ne pas supprimer ce profil. Exporter chaque scénario en JSON
avant une mise à niveau reste une solution de secours.

Le laboratoire écrit v5 et lit v1–v5 ; le Proto 2 écrit v3 et lit v1/v2/v3 dans un
stockage distinct. Le navigateur possède aussi son propre stockage : utiliser
l'export/import pour transférer une partie du site vers l'application.

Les versions précédentes restent disponibles dans les releases. Une ancienne
application peut ne pas lire un format plus récent : garder ses exports antérieurs
avant de revenir à une version précédente.

`verification.json` identifie les fichiers effectivement testés sous Windows,
leurs empreintes et les contrôles réalisés. Les fichiers publiés ne sont pas
reconstruits après les tests. Les artefacts de test Actions sont conservés 14 jours ;
les fichiers des releases ne sont pas soumis à cette expiration.

Ce dépôt public contient les distributions et leurs instructions. Le dépôt source
et les documents du créateur restent privés. Les travaux d'autres branches ne sont
pas incorporés à cette distribution.

[Version navigateur](https://dynasty-test-rouge.vercel.app/?scenario=proto2)
