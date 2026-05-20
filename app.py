from app_factory import create_app, db

app = create_app()


@app.cli.command("init-db")
def init_db():
    """Create database tables for local development."""
    db.create_all()
    print("Database initialized.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)