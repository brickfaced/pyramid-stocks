from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/index.jinja2')
def get_home_view(request):
    return {}


@view_config(route_name='auth', renderer='../templates/login.jinja2')
def get_auth_view(request):
    return {}


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2')
def get_stock_view(request):
    return {}


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def get_portfolio(request):
    return {}


@view_config(route_name='portfoliosymbol', renderer='../templates/portfolio.jinja2')
def get_portfolo_symbol_view(request):
    return {}
