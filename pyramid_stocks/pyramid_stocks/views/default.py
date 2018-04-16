# from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from . import DB_ERR_MSG
from sqlalchemy.exc import DBAPIError
from ..models import Stock
from ..models import Account
import requests
from pyramid.response import Response
from pyramid.security import NO_PERMISSION_REQUIRED


API_URL = 'https://api.iextrading.com/1.0'


@view_config(
    route_name='home',
    renderer='../templates/base.jinja2',
    permission=NO_PERMISSION_REQUIRED)
def get_home_view(request):
    return {}


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def get_portfolio_view(request):
    try:
        query = request.dbsession.query(Account)
        user_stocks = query.filter(Account.username == request.authenticated_userid).first()
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)
    if user_stocks:
        return {'portfolio': user_stocks.stock_id}
    else:
        return HTTPNotFound()


@view_config(route_name='details', renderer='../templates/details.jinja2',)
def get_detail_view(request):
    try:
        stock_symbol = request.matchdict['symbol']
    except KeyError:
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
    if request.method == 'POST':
        fields = ['symbol']

        if not all([field in request.POST for field in fields]):
            raise HTTPBadRequest

        query = request.dbsession.query(Account)
        instance = query.filter(Account.username == request.authenticated_userid).first()

        query = request.dbsession.query(Stock)
        instance2 = query.filter(Stock.symbol == request.POST['symbol']).first()

        if instance2:
            instance2.account_id.append(instance)
        else:
            new = Stock()
            new.account_id.append(instance)
            new.symbol = request.POST['symbol']
            new.companyName = request.POST['companyName']
            new.exchange = request.POST['exchange']
            new.industry = request.POST['industry']
            new.website = request.POST['website']
            new.description = request.POST['description']
            new.CEO = request.POST['CEO']
            new.issueType = request.POST['issueType']
            new.sector = request.POST['sector']

            try:
                request.dbsession.add(new)
                request.dbsession.flush()
            except DBAPIError:
                return Response(DB_ERR_MSG, content_type='text/plain', status=500)

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()

    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}

        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        return {'company': data}
