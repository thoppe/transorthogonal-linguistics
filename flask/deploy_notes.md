Demo the app locally by running and visiting http://0.0.0.0:5000

    foreman start

Numpy is required, which requires BLAS and LAPACK
  
    heroku config:set BUILDPACK_URL=https://github.com/thenovices/heroku-buildpack-scipy

Since the heroku app is stored in the /flask directory, we can push the subtree only to Heroku with the following command (this has to run in the root dir):

    git subtree push --prefix flask heroku master


  