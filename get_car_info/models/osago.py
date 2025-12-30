from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Driver(BaseModel):
    fullname: str = Field(alias="fullName")


class OsagoModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
        
    masked_phone: str = Field(alias="maskedPhone")
    username: str = Field(alias="userName")
    brand_name: str = Field(alias="brandName")
    model_name: str = Field(alias="modelName")
    order_hash: str = Field(alias="orderHash")
    company_id: int = Field(alias="companyId")
    product_id: int = Field(alias="productId")
    company_name: str = Field(alias="companyName")
    price: int
    previous_policy_number: str = Field(alias="previousPolicyNumber")
    vehicle_year: int = Field(alias="vehicleYear")
    policyend_date: str = Field(alias="policyEndDate")
    drivers: list[Driver]
    drivers_amount: int = Field(alias="driversAmount")
    car_number: str = Field(alias="carNumber")
