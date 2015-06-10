Demo the app locally by running and visiting http://0.0.0.0:5000

    foreman start

Start the app creation

    heroku create transorthogonal-linguistics
    
Since the heroku app is stored in the /flask directory, we can push the subtree only to Heroku with the following command (this has to run in the root dir):

    git subtree push --prefix flask heroku master

If scipy/numpy is required they require BLAS and LAPACK
  
    heroku config:set BUILDPACK_URL=https://github.com/thenovices/heroku-buildpack-scipy

