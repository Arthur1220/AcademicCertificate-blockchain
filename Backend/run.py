from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Configuração carregada:", app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(debug=True)
