from src import main

if __name__ == "__main__":
    app = main.generate_cli_server()()

    @app.default
    def default_action():
        print("This is the Script Base for current project")

    app()
