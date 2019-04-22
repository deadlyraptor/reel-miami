# run.py

from reel_miami import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
