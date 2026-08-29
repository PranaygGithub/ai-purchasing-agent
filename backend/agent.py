from .models import Scenario1Request, Scenario1Response, Scenario2Request, Scenario2Response
from .validation import validate_scenario1, validate_scenario2


def money(value: float) -> str:
    return f"${value:,.2f}"


def analyze_scenario1(r: Scenario1Request) -> Scenario1Response:
    factors = []
    risks = []

    inventory_position = r.current_inventory + r.open_purchase_orders
    projected_after_demand = inventory_position - r.expected_demand
    storage_after_purchase = inventory_position + r.recommended_quantity
    purchase_cost = r.recommended_quantity * r.unit_price

    factors.append(f"Inventory position = {inventory_position} units.")
    factors.append(f"Projected stock after expected demand = {projected_after_demand} units.")
    factors.append(f"Supplier lead time = {r.supplier_lead_time_days} days.")
    factors.append(f"Supplier MOQ = {r.supplier_minimum_order} units.")
    factors.append(f"Purchase cost = {money(purchase_cost)}.")
    factors.append(
        f"Storage after proposed purchase = "
        f"{storage_after_purchase}/{r.storage_capacity} units."
    )

    budget_ok = purchase_cost <= r.available_budget
    storage_ok = storage_after_purchase <= r.storage_capacity
    moq_ok = r.recommended_quantity >= r.supplier_minimum_order

    if not budget_ok:
        risks.append("Budget constraint: proposed purchase exceeds available budget.")
    if not storage_ok:
        risks.append("Storage constraint: proposed purchase exceeds available capacity.")
    if not moq_ok:
        risks.append("Supplier MOQ: proposed quantity is below the minimum order.")
    if projected_after_demand >= 0:
        risks.append(
            "Inventory may already cover expected demand after open purchase orders."
        )

    if not budget_ok:
        decision = "REJECT"
        approved = 0
        action = "Do not create the recommended purchase order."
        summary = "Reject because the proposed purchase exceeds the available budget."

    elif storage_ok and projected_after_demand < 0 and moq_ok:
        decision = "ACCEPT"
        approved = r.recommended_quantity
        action = f"Approve the recommended quantity of {approved} units."
        summary = (
            "The recommendation is feasible and addresses the projected demand gap."
        )

    else:
        decision = "MODIFY"
        demand_gap = max(0, r.expected_demand - inventory_position)
        quantity = max(demand_gap, r.supplier_minimum_order)
        quantity = min(quantity, r.recommended_quantity)

        if quantity <= 0:
            decision = "REJECT"
            approved = 0
            action = "Do not purchase; existing inventory and open POs are sufficient."
            summary = (
                "The recommendation is unnecessary based on the current inventory position."
            )
        elif quantity * r.unit_price > r.available_budget:
            decision = "REJECT"
            approved = 0
            action = "Do not execute; investigate a lower-cost or budget-approved option."
            summary = "A compliant purchase quantity cannot be executed within budget."
        elif inventory_position + quantity > r.storage_capacity:
            decision = "INVESTIGATE"
            approved = 0
            action = "Investigate storage release or a smaller replenishment plan."
            summary = (
                "Demand exists, but storage capacity prevents safe execution."
            )
        else:
            approved = quantity
            action = f"Modify the purchase order to {quantity} units."
            summary = (
                "The agent reduced the recommendation to align with demand and constraints."
            )

    validation_passed, validation_message = validate_scenario1(
        r, approved, decision
    )

    return Scenario1Response(
        scenario="Scenario 1 — Purchase Recommendation Review",
        decision=decision,
        recommended_quantity=r.recommended_quantity,
        approved_quantity=approved,
        action=action,
        summary=summary,
        important_factors=factors,
        risks=risks,
        validation_passed=validation_passed,
        validation_message=validation_message,
    )


def analyze_scenario2(r: Scenario2Request) -> Scenario2Response:
    factors = []
    risks = []

    shortfall = max(0, r.original_purchase_order - r.supplier_confirmed_quantity)
    inventory_after_demand = r.current_inventory - r.expected_demand

    factors.append(f"Original PO = {r.original_purchase_order} units.")
    factors.append(f"Supplier confirmed = {r.supplier_confirmed_quantity} units.")
    factors.append(f"Supplier shortfall = {shortfall} units.")
    factors.append(
        f"Inventory after expected demand = {inventory_after_demand} units."
    )
    factors.append(
        f"Alternative supplier available = {r.alternative_supplier_available}."
    )

    if shortfall == 0:
        decision = "ACCEPT"
        alternative_quantity = 0
        action = "Continue with the existing purchase order."
        summary = "The supplier can fulfil the full purchase order."
    elif inventory_after_demand >= shortfall:
        decision = "ACCEPT PARTIAL + WAIT"
        alternative_quantity = 0
        action = (
            f"Accept {r.supplier_confirmed_quantity} units and cover the shortfall "
            "from existing inventory."
        )
        summary = (
            "Current inventory can absorb the supplier shortfall without another purchase."
        )
        risks.append("Inventory buffer will be reduced after covering expected demand.")
    elif (
        r.alternative_supplier_available
        and r.alternative_supplier_quantity >= shortfall
        and shortfall * r.alternative_supplier_unit_price <= r.available_budget
    ):
        decision = "SOURCE REMAINDER"
        alternative_quantity = shortfall
        action = (
            f"Accept {r.supplier_confirmed_quantity} units from the current supplier "
            f"and source {shortfall} units from the alternative supplier."
        )
        summary = (
            "The shortfall can be covered by an available alternative supplier within budget."
        )
        risks.append(
            f"Alternative supplier price is {money(r.alternative_supplier_unit_price)} per unit."
        )
    elif r.alternative_supplier_available:
        decision = "INVESTIGATE"
        alternative_quantity = 0
        action = (
            "Request alternative supplier pricing/quantity confirmation "
            "before creating another PO."
        )
        summary = (
            "An alternative supplier exists, but quantity or budget has not been proven sufficient."
        )
        risks.append("Additional supplier information is required before execution.")
    else:
        decision = "ESCALATE"
        alternative_quantity = 0
        action = (
            "Escalate the shortfall to a buyer for sourcing or replenishment decision."
        )
        summary = (
            "Neither inventory nor an alternative supplier can safely cover the shortfall."
        )
        risks.append("Potential stock-out risk.")

    validation_passed, validation_message = validate_scenario2(
        r, shortfall, alternative_quantity, decision
    )

    return Scenario2Response(
        scenario="Scenario 2 — Supplier Cannot Fulfil the Purchase",
        decision=decision,
        original_quantity=r.original_purchase_order,
        confirmed_quantity=r.supplier_confirmed_quantity,
        shortfall=shortfall,
        alternative_quantity=alternative_quantity,
        action=action,
        summary=summary,
        important_factors=factors,
        risks=risks,
        validation_passed=validation_passed,
        validation_message=validation_message,
    )
