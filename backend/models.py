from pydantic import BaseModel, Field
from typing import Literal


class Scenario1Request(BaseModel):
    product: str = Field(min_length=1)
    recommended_quantity: int = Field(gt=0)
    current_inventory: int = Field(ge=0)
    expected_demand: int = Field(ge=0)
    open_purchase_orders: int = Field(ge=0)
    supplier_lead_time_days: int = Field(ge=0)
    supplier_minimum_order: int = Field(ge=0)
    available_budget: float = Field(ge=0)
    unit_price: float = Field(ge=0)
    storage_capacity: int = Field(gt=0)


class Scenario1Response(BaseModel):
    scenario: str
    decision: Literal["ACCEPT", "MODIFY", "REJECT", "INVESTIGATE"]
    recommended_quantity: int
    approved_quantity: int
    action: str
    summary: str
    important_factors: list[str]
    risks: list[str]
    validation_passed: bool
    validation_message: str


class Scenario2Request(BaseModel):
    product: str = Field(min_length=1)
    original_purchase_order: int = Field(gt=0)
    supplier_confirmed_quantity: int = Field(ge=0)
    current_inventory: int = Field(ge=0)
    expected_demand: int = Field(ge=0)
    alternative_supplier_available: bool
    alternative_supplier_quantity: int = Field(ge=0)
    alternative_supplier_unit_price: float = Field(ge=0)
    current_supplier_unit_price: float = Field(ge=0)
    available_budget: float = Field(ge=0)


class Scenario2Response(BaseModel):
    scenario: str
    decision: Literal[
        "ACCEPT",
        "ACCEPT PARTIAL + WAIT",
        "SOURCE REMAINDER",
        "INVESTIGATE",
        "ESCALATE",
    ]
    original_quantity: int
    confirmed_quantity: int
    shortfall: int
    alternative_quantity: int
    action: str
    summary: str
    important_factors: list[str]
    risks: list[str]
    validation_passed: bool
    validation_message: str
