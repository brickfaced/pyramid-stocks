import pytest
from pyramid import testing
from ..models.meta import Base
from ..models import Stock, Account


@pytest.fixture
def test_stock():
    return Stock(
        symbol='Test',
        companyName='Test',
        exchange='Test',
        industry='Test',
        website='Test',
        description='Test',
        CEO='Test',
        issueType='Test',
        sector='Test',
    )


@pytest.fixture
def test_account():
    return Account(
        username='brickfaced', email='brickfazed@hotmail.com', password='password'
    )


@pytest.fixture
def configuration(request):
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://postgres:password@localhost:5432/pyramid_stocks_test'
    })
    config.include('pyramid_stocks.models')
    config.include('pyramid_stocks.routes')

    config.testing_securitypolicy(
        userid="brickfaced",
        permissive=True,
    )

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    return testing.DummyRequest(dbsession=db_session)
