import pytest


@pytest.fixture
@pytest.mark.django_db
def user_csrf(client, django_user_model):
    username = 'user'
    # first_name = ''
    # last_name = ''
    # email = 'user@user.com'
    password = 'mypassword20'

    django_user_model.objects.create_user(
        username=username,
        password=password
    )

    response = client.post(
        '/core/login',
        {
            "username": username,
            "password": password
        },
        format='json'
    )

    return