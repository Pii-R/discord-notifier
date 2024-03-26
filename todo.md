Continuer à mettre en place la logique de notifications au premier lancement du bot

- vérifier le lien entre UserSettings et Notifications
- commande pour afficher toutes les notifications disponibles
- subscribe de base à la notification 1
- sinon mettre la possibilité de changer
- décoder crontab pour avoir la prochaine exécution, faire attention au timezone mettre utc ?
- mettre un !stop et un !resume afin de gérer les notifications et pas se désinscrire
- mettre un champ is_active is_running dans user_settings afin de savoir si la notification est active
- command pause all, resume all
- commande pour que l'utilisateur connaisse les tâches aux quelles il a souscris
- mettre un help <command>
- utiliser github pages afin de partager l'adresse du bot
- ajout d'un timezone dans la base pour déterminer l'heure d'envoi. Par défaut UTC+2 Paris
  - mettre une liste des timezones et proposer à l'utilisateur de choisir parmis sa liste afin de définir son timezone.
- problème de l'appel de `TaskHandler` lors du on_message. En effet, l'appel du task handler est fait à chaque message de n'importe quel utilisateur. De fait, il faut vérifier l'entrée de l'utilisateur afin de n'appeler task handler que sur des messages qui peuvent déclenche une modification des tâches. Fait mais à vérifier car les tests ne passent plus. Déporter la logique ailleurs.
