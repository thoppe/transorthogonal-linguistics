Demo the app locally by running and visiting http://0.0.0.0:5000

    foreman start

-------------------------------------------------------------------------

Start the app creation

    heroku create transorthogonal-linguistics
    
Use the branch "flask" to create the app. Push the app branch with:

    git push heroku flask:master

If scipy/numpy is required they require BLAS and LAPACK
  
    heroku config:set BUILDPACK_URL=https://github.com/thenovices/heroku-buildpack-scipy

