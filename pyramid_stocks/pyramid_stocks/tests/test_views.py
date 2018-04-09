def test_default_behavior_of_home_view(dummy_request):
    from ..views.default import get_home_view
    response = get_home_view(dummy_request)
    assert isinstance(response, dict)
    assert response == {}


def test_default_behavior_of_auth_view(dummy_request):
    from ..views.default import get_auth_view
    response = get_auth_view(dummy_request)
    assert isinstance(response, dict)
    assert response == {}


def test_default_behavior_of_portfolio_view(dummy_request):
    from ..views.default import get_portfolio_view
    response = get_portfolio_view(dummy_request)
    assert type(response) == dict
    assert response['portfolio'][0]['companyName'] == 'Kojima Productions'
