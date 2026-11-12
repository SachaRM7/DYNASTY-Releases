DYNASTY Windows : Portable et Installer, avec réglage des mises à jour.

Dans **Sauvegardes et réglages → Mises à jour** :

- Interrupteur désactivé : recherche et téléchargement uniquement à votre demande.
- Interrupteur activé : recherche au lancement puis périodiquement, téléchargement en arrière-plan.
- Une confirmation reste nécessaire avant installation. Le jeu sauvegarde avant de redémarrer.
- Le Portable conserve son emplacement ; une copie `.previous` de l'exécutable est conservée.

Les versions antérieures sans cet updater doivent être remplacées ou mises à niveau
une première fois manuellement. Aucun compte GitHub, Node.js ou terminal n'est nécessaire
pour jouer. Les deux formats partagent `%APPDATA%\DYNASTY-Prototype` et l'origine
`dynasty://game/`. Ne supprimez pas ce profil. Un export JSON manuel reste disponible.

Les exécutables ne disposent pas d'une signature d'éditeur Microsoft (Authenticode).
Le manifeste de mise à jour est signé Ed25519 et les téléchargements sont vérifiés
par l'application. Aucun abonnement ni certificat Windows payant n'est nécessaire.
Les avertissements Windows éventuels ne sont pas supprimés par cette signature.

Le contenu reste celui du Proto 2 (1850), avec le laboratoire historique J1–J4 (1852).
Cette distribution n'intègre pas les travaux graphiques ou de gameplay d'autres branches.
Le format Proto 2 v3 relit v1/v2 ; le laboratoire v5 relit v1/v2/v3/v4.
Les sources documentaires privées ne sont pas incluses.

`verification.json` identifie les fichiers testés et leurs preuves. Les fichiers
publiés sont repris tels quels des tests Windows, sans reconstruction lors de la publication.

Contrôle après publication : les deux distributions ont réellement téléchargé et
installé cette version depuis le canal GitHub public sur Windows. Les sauvegardes
complètes des deux scénarios et le réglage automatique sont conservés. Le départ
0.6.2 est une version de test équipée du nouvel updater, pas une ancienne version
publiée. [Résultat détaillé](https://github.com/SachaRM7/DYNASTY-Releases/blob/work/windows-auto-updates/PUBLIC-UPDATE-VERIFICATION.json).
