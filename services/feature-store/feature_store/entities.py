from feast import Entity

customer = Entity(
    name="customer",
    join_keys=["customer_id"],
    description="Customer ID",
)
