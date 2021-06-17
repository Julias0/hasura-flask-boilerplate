from app import create_app
app = create_app()

if __name__ == '__main__':
    import os
    app.run(port=os.getenv('PORT'), debug=True)