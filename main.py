from website import create_app

app = create_app()

if __name__ == '__main__': #if we run this file
    app.run(debug=True) # we run the flask application ( everytime we change code it reruns the server)

