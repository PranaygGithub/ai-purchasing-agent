def validate_scenario1(request, approved_quantity: int, decision: str) -> tuple[bool, str]:
    if decision in {"REJECT", "INVESTIGATE"}:
        return approved_quantity == 0, (
            "Validated: no purchase action is proposed while the case is rejected/investigated."
            if approved_quantity == 0
            else "Validation failed: rejected/investigated case has a purchase quantity."
        )

    cost = approved_quantity * request.unit_price
    storage_after = (
        request.current_inventory
        + request.open_purchase_orders
        + approved_quantity
    )

    valid = (
        approved_quantity >= request.supplier_minimum_order
        and cost <= request.available_budget
        and storage_after <= request.storage_capacity
    )

    if valid:
        return True, "Validated: proposed quantity satisfies MOQ, budget and storage constraints."

    return False, "Validation failed: proposed quantity violates a hard purchasing constraint."


def validate_scenario2(request, shortfall: int, alternative_quantity: int, decision: str) -> tuple[bool, str]:
    if decision == "ACCEPT":
        valid = shortfall == 0
    elif decision == "ACCEPT PARTIAL + WAIT":
        valid = request.current_inventory - request.expected_demand >= shortfall
    elif decision == "SOURCE REMAINDER":
        valid = (
            alternative_quantity == shortfall
            and alternative_quantity <= request.alternative_supplier_quantity
            and alternative_quantity * request.alternative_supplier_unit_price
            <= request.available_budget
        )
    else:
        valid = alternative_quantity == 0

    if valid:
        return True, "Validated: the proposed supplier-shortfall action is internally consistent."

    return False, "Validation failed: the proposed action is not supported by the available data."
