from flask import Flask


def create_app():
    """Construct core Flask app."""
    # Create Flask's `app` object
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder="templates"
    )
    app.config.from_pyfile('config.py')

    with app.app_context():
        # Import parts of our app
        import routes
        import example

        return app
