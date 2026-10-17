import pytest
from app.services.earnings_service import calculate_net_earnings

def test_calculate_net_earnings_standard():
    # Example: Delivery partner gross ₹850, tips ₹120, fuel/maintenance ₹220
    net = calculate_net_earnings(850.0, 120.0, 220.0)
    assert net == 750.0

def test_calculate_net_earnings_zero_tips():
    net = calculate_net_earnings(500.0, 0.0, 150.0)
    assert net == 350.0

def test_calculate_net_earnings_zero_expenses():
    net = calculate_net_earnings(600.0, 50.0, 0.0)
    assert net == 650.0

def test_calculate_net_earnings_expenses_exceed_gross():
    # If a driver had bad day with repair
    net = calculate_net_earnings(400.0, 0.0, 650.0)
    assert net == -250.0

def test_calculate_net_earnings_rounding():
    net = calculate_net_earnings(100.333, 10.555, 20.111)
    # 100.333 + 10.555 - 20.111 = 90.777 -> round to 90.78
    assert net == 90.78
