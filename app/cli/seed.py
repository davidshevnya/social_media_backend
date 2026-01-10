import click

from app.extensions import db
from app.models import User

@click.group()
def seed():
    """Database seeding commands"""
    pass

@seed.command('users')
def seed_users():
    users = [
        User(username='alice', email='alice@email.com', password_hash='hashed'),
        User(username='bob', email='bob@email.com', password_hash='hashed'),
    ]
    db.session.add_all(users)
    try:
        db.session.commit()
    except db.exc.IntegrityError:
        click.echo('u already seeded users!')
        return db.session.rollback()
    click.echo('Seeded users!')
