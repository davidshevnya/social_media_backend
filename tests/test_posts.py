import pytest

from .utils import register_and_login

@pytest.mark.parametrize('title, content, status_code', [
    ('First test title', 'First test content', 201),
    ('', 'imdumbass', 201),
    ('Post title', '', 400),
    ('imgay'*69, '', 400),
    ('', 'imgay', 201)
])
def test_create_post(client, title, content, status_code):
    token =  register_and_login(client)
    
    # Create post
    response = client.post('posts/create', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'title': f'{title}',
        'content': f'{content}'
    })
    
    post = response.json.get('post')
    
    assert response.status_code == status_code
    if status_code == 201:
        assert post.get('title') == title
        assert post.get('content') == content
        
def test_get_post(client):
    token = register_and_login(client)
    
    # create post
    response = client.post('posts/create', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'title': 'test title',
        'content': 'test content'
    })
    
    assert response.status_code == 201
    
    # get post
    response = client.get('/posts/1', headers={
        'Authorization': f'Bearer {token}'
    })
    
    post = response.json.get('post')
    
    assert response.status_code == 200
    assert post.get('title') == 'test title'
    assert post.get('content') == 'test content'
    
def test_get_user_posts(client):
    token = register_and_login(client)
    
    # Create post
    response = client.post('posts/create', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'title': 'test title',
        'content': 'test content'
    })
    
    # get user posts
    response = client.get('/posts/user/1', headers={
        'Authorization': f'Bearer {token}'
    })
    
    posts = response.json.get('posts')
    
    assert response.status_code == 200
    assert posts[0]['title'] == 'test title' 
    assert posts[0]['content'] == 'test content' 
    
    
def test_post(client):
    token =  register_and_login(client)
    
    # Create post
    response = client.post('posts/create', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'title': 'test title',
        'content': 'test content'
    })
    
    # Edit post
    response = client.put('/posts/1/edit', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'title': 'iamgay',
        'content': 'iloveboys'
    })
    
    assert response.status_code == 200
    user = response.json.get('post')
    assert user.get('title') == 'iamgay'
    assert user.get('content') == 'iloveboys'
    