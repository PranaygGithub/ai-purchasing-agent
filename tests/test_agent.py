from backend.models import Scenario1Request, Scenario2Request
from backend.agent import analyze_scenario1, analyze_scenario2


def test_scenario1_accepts_feasible_recommendation():
    request = Scenario1Request(
        product="Coffee",
        recommended_quantity=800,
        current_inventory=100,
        expected_demand=700,
        open_purchase_orders=0,
        supplier_lead_time_days=5,
        supplier_minimum_order=100,
        available_budget=20000,
        unit_price=10,
        storage_capacity=1200,
    )

    result = analyze_scenario1(request)

    assert result.decision == "ACCEPT"
    assert result.approved_quantity == 800
    assert result.validation_passed is True


def test_scenario1_rejects_budget_failure():
    request = Scenario1Request(
        product="Coffee",
        recommended_quantity=800,
        current_inventory=100,
        expected_demand=1000,
        open_purchase_orders=0,
        supplier_lead_time_days=5,
        supplier_minimum_order=100,
        available_budget=1000,
        unit_price=10,
        storage_capacity=2000,
    )

    result = analyze_scenario1(request)

    assert result.decision == "REJECT"
    assert result.approved_quantity == 0
    assert result.validation_passed is True


def test_scenario1_modifies_when_existing_supply_is_enough():
    request = Scenario1Request(
        product="Coffee",
        recommended_quantity=800,
        current_inventory=500,
        expected_demand=600,
        open_purchase_orders=300,
        supplier_lead_time_days=5,
        supplier_minimum_order=100,
        available_budget=20000,
        unit_price=10,
        storage_capacity=2000,
    )

    result = analyze_scenario1(request)

    assert result.decision == "MODIFY"
    assert result.approved_quantity == 100
    assert result.validation_passed is True


def test_scenario2_sources_remainder():
    request = Scenario2Request(
        product="Milk",
        original_purchase_order=500,
        supplier_confirmed_quantity=250,
        current_inventory=50,
        expected_demand=400,
        alternative_supplier_available=True,
        alternative_supplier_quantity=300,
        alternative_supplier_unit_price=12,
        current_supplier_unit_price=10,
        available_budget=10000,
    )

    result = analyze_scenario2(request)

    assert result.decision == "SOURCE REMAINDER"
    assert result.shortfall == 250
    assert result.alternative_quantity == 250
    assert result.validation_passed is True


def test_scenario2_uses_inventory():
    request = Scenario2Request(
        product="Milk",
        original_purchase_order=500,
        supplier_confirmed_quantity=250,
        current_inventory=700,
        expected_demand=300,
        alternative_supplier_available=False,
        alternative_supplier_quantity=0,
        alternative_supplier_unit_price=0,
        current_supplier_unit_price=10,
        available_budget=10000,
    )

    result = analyze_scenario2(request)

    assert result.decision == "ACCEPT PARTIAL + WAIT"
    assert result.validation_passed is True


def test_scenario2_escalates_without_coverage():
    request = Scenario2Request(
        product="Milk",
        original_purchase_order=500,
        supplier_confirmed_quantity=100,
        current_inventory=50,
        expected_demand=500,
        alternative_supplier_available=False,
        alternative_supplier_quantity=0,
        alternative_supplier_unit_price=0,
        current_supplier_unit_price=10,
        available_budget=10000,
    )

    result = analyze_scenario2(request)

    assert result.decision == "ESCALATE"
    assert result.validation_passed is True
