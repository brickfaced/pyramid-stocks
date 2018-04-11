# from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from . import DB_ERR_MSG
from sqlalchemy.exc import DBAPIError
from ..models import Stock
import requests
from pyramid.response import Response


API_URL = 'https://api.iextrading.com/1.0'


@view_config(route_name='home', renderer='../templates/base.jinja2')
def get_home_view(request):
    return {}


@view_config(route_name='auth', renderer='../templates/auth.jinja2')
def get_auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))
            return HTTPFound(location=request.route_url('portfolio'))

        except KeyError:
            return {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('User: {}, Pass: {}'.format(username, password))
        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def get_portfolio_view(request):
    try:
        query = request.dbsession.query(Stock)
        all_stocks = query.all()
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

    return {'portfolio': all_stocks}


@view_config(route_name='details', renderer='../templates/details.jinja2')
def get_detail_view(request):
    try:
        stock_symbol = request.matchdict['symbol']
    except IndexError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        stock_detail = query.filter(Stock.symbol == stock_symbol).first()
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

    return {
        "stock": stock_detail,
    }


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2')
def get_stock_view(request):
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}

        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        return {'company': data}

    if request.method == 'POST':
        fields = ['symbol']

        if not all([field in request.POST for field in fields]):
            return HTTPBadRequest()

        instance = {
            'symbol': request.POST['symbol'],
            'companyName': request.POST['companyName'],
            'exchange': request.POST['exchange'],
            'industry': request.POST['industry'],
            'website': request.POST['website'],
            'description': request.POST['description'],
            'CEO': request.POST['CEO'],
            'issueType': request.POST['issueType'],
            'sector': request.POST['sector']
        }
        instance = Stock(**instance)

        try:
            request.dbsession.add(instance)
        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

        return HTTPFound(location=request.route_url('portfolio'))
