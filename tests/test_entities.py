from unittest import TestCase

from src.views.dolibarr.entities import DolibarrEntitiesView


class TestEntities(TestCase):
    def test_get_stocked_and_for_sale_with_missing_external_ref(self):
        e = DolibarrEntitiesView()
        assert len(e.get_stocked_and_for_sale_with_missing_external_ref()) == 4
