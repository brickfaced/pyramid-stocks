def test_entry_to_stocks(db_session):
    from .. models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol='yo',
        companyName='sup',
        exchange='qvo',
        industry='nothin',
        website='nada',
        description='Test',
        CEO='Test',
        issueType='Test',
        sector='Test'
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_entry_to_stocks_with_no_symbol_throws_error(db_session):
    from ..models import Stock
    import pytest
    from sqlalchemy.exc import IntegrityError

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        companyName='sup',
        exchange='qvo',
        industry='nothin',
        website='nada',
        description='Test',
        CEO='Test',
        issueType='Test',
        sector='Test'
    )
    with pytest.raises(IntegrityError):
        db_session.add(stock)

        assert db_session.query(Stock).one_or_none() is None
