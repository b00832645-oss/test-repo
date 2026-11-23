"""Integration tests: OrderService + a real ProductRepository working together."""


class TestIntegrationOrderService:
    def test_successful_order(self, order_service):
        # Act
        result = order_service.place_order("SHIRT", 2)
        # Assert: 2 x 25 = 50, + 20 % tax = 60
        assert result == {"success": True, "item": "T-Shirt", "quantity": 2, "total": 60.0}

    def test_stock_is_reduced_after_order(self, order_service):
        order_service.place_order("MUG", 3)
        assert order_service.repo.get_product("MUG")["stock"] == 97

    def test_unknown_product(self, order_service):
        assert order_service.place_order("PANTS", 1) == {"success": False, "error": "Product not found"}

    def test_order_exceeds_stock_changes_nothing(self, order_service):
        result = order_service.place_order("HAT", 999)
        assert result["error"] == "Not enough stock"
        assert order_service.repo.get_product("HAT")["stock"] == 30

    def test_multiple_orders_deplete_stock(self, order_service):
        order_service.place_order("HAT", 10)
        order_service.place_order("HAT", 15)
        assert order_service.repo.get_product("HAT")["stock"] == 5

    def test_each_test_gets_a_fresh_repository(self, order_service):
        # If fixtures were shared, the previous test would have left HAT at 5.
        assert order_service.repo.get_product("HAT")["stock"] == 30

    def test_non_positive_quantity(self, order_service):
        assert order_service.place_order("MUG", 0)["success"] is False
