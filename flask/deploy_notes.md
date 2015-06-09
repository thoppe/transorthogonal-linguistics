Since the heroku app is stored in the /flask directory, we can push the subtree only to Heroku with the following command:

  git subtree push --prefix output heroku master