def register_and_login(client):
    # register and login
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })

    login_response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })

    return login_response