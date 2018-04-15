from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest, HTTPUnauthorized


def test_default_behavior_of_home_view(dummy_request):
    from ..views.default import get_home_view

    response = get_home_view(dummy_request)
    assert isinstance(response, dict)
    assert response == {}


def test_default_behavior_of_auth_view(dummy_request):
    from ..views.auth import get_auth_view

    response = get_auth_view(dummy_request)
    assert isinstance(response, dict)
    assert response == {}


def test_auth_unauthorized_view(dummy_request):
    from ..views.auth import get_auth_view

    dummy_request.GET = {'username': 'stonefaced', 'password': 'password'}
    response = get_auth_view(dummy_request)
    assert response.status_code == 401
    assert isinstance(response, HTTPUnauthorized)


def test_auth_bad_signup_view(dummy_request):
    from ..views.auth import get_auth_view

    dummy_request.method = 'POST'
    dummy_request.POST = {'username': 'Noob', 'password': 'password'}
    response = get_auth_view(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_behavior_of_portfolio_view(dummy_request):
    from ..views.default import get_portfolio_view

    response = get_portfolio_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_behavior_of_detail_view(dummy_request, db_session, test_stock):
    from ..views.default import get_detail_view

    db_session.add(test_stock)
    dummy_request.matchdict = {'symbol': 'Test'}
    response = get_detail_view(dummy_request)
    assert type(response) == dict
    assert response['stock'].symbol == 'Test'
    assert response['stock'].companyName == 'Test'


def test_detail_not_found(dummy_request):
    from ..views.default import get_detail_view
    from pyramid.httpexceptions import HTTPNotFound

    response = get_detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_behavior_add_stock(dummy_request):
    from ..views.default import get_stock_view

    response = get_stock_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


def test_behavior_post_add_stock(dummy_request, db_session, test_account):
    from ..views.default import get_stock_view

    db_session.add(test_account)

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'symbol': 'yo',
        'companyName': 'sup',
        'exchange': 'qvo',
        'industry': 'nothin',
        'website': 'nada',
        'description': 'Test',
        'CEO': 'Test',
        'issueType': 'Test',
        'sector': 'Test'
    }

    response = get_stock_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_add_stock_adds_to_db(dummy_request, db_session, test_account):
    from ..views.default import get_stock_view
    from ..models import Stock

    db_session.add(test_account)

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'symbol': 'yo',
        'companyName': 'sup',
        'exchange': 'qvo',
        'industry': 'nothin',
        'website': 'nada',
        'description': 'Test',
        'CEO': 'Test',
        'issueType': 'Test',
        'sector': 'Test'
    }

    get_stock_view(dummy_request)
    query = db_session.query(Stock)
    one = query.first()
    assert one.symbol == 'yo'
    assert one.companyName == 'sup'
    assert type(one.id) == int


def test_invalid_post_to_db(dummy_request):
    import pytest
    from ..views.default import get_stock_view

    dummy_request.method = 'POST'
    dummy_request.POST = {}

    with pytest.raises(HTTPBadRequest):
        response = get_stock_view(dummy_request)
        assert isinstance(response, HTTPBadRequest)
