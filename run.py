from app import create_app

# Cria a instância da aplicação
app = create_app()

if __name__ == '__main__':
    # Roda a aplicação no modo de desenvolvimento
    app.run(debug=True)