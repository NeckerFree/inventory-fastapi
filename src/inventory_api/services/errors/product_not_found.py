class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
            self.product_id=product_id
            super().__init__(f"Product with ID {product_id} does not exist")
