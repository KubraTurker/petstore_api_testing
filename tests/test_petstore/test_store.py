import time
import pytest
from fixtures.petstore.store.model import Order


class TestStore:

    @pytest.mark.positive
    def test_add_order(self, app):
        """
        Yeni bir sipariş ekleme testi.
        Adımlar:
            1. Yeni bir sipariş nesnesi oluştur.
            2. Siparişi mağazaya ekle.
            3. Yanıtın 200 (veya 201) olduğunu doğrula.
            4. Yanıttaki sipariş kimliğini doğrula.
        """
        data = Order.random()
        res = app.store_api.add_order(data=data)

        assert res.status_code == 200  # veya 201
        assert isinstance(res.data, Order), "Yanıt verisi Order nesnesi değil"
        assert res.data.id == data.id, "Sipariş kimliği eşleşmiyor"

    @pytest.mark.positive
    def test_get_order_by_id(self, app):
        """
        Sipariş ID ile alma testi.
        Adımlar:
            1. Yeni bir sipariş nesnesi oluştur.
            2. Siparişi mağazaya ekle.
            3. Siparişi ID ile getir.
            4. Yanıtın 200 olduğunu doğrula.
            5. Getirilen siparişin ID'sini doğrula.
        """
        data = Order.random()
        res_add = app.store_api.add_order(data=data)
        assert res_add.status_code == 200  # veya 201

        res_get = app.store_api.get_order_by_id(
            order_id=res_add.data.id, type_response=Order
        )

        time.sleep(2)

        assert res_get.status_code == 200, "Get isteği başarısız"
        assert isinstance(res_get.data, Order), "Yanıt verisi Order nesnesi değil"
        assert res_get.data.id == data.id, "Sipariş kimliği eşleşmiyor"

    @pytest.mark.positive
    def test_delete_order(self, app):
        """
        Sipariş silme testi.
        Adımlar:
            1. Yeni bir sipariş nesnesi oluştur.
            2. Siparişi mağazaya ekle.
            3. Siparişi sil.
            4. Silinen siparişi ID ile çağır.
            5. Silme işleminin başarılı olduğunu doğrula.
            6. Silinen siparişin artık mevcut olmadığını doğrula (404 dönmeli).
        """
        data = Order.random()
        res_add = app.store_api.add_order(data=data)
        assert res_add.status_code == 200  # veya 201

        time.sleep(5)

        res_delete = app.store_api.delete_order(order_id=res_add.data.id)
        assert res_delete.status_code == 200, "Silme işlemi başarısız"

        print(f"Silme yanıtı: {res_delete.json()}")

        res_get = app.store_api.get_order_by_id(order_id=data.id)

        if res_get.status_code == 200:
            print(f"Sipariş silindikten sonra hala mevcut, yanıt: {res_get.json()}")

        assert (
            res_get.status_code == 404
        ), f"Sipariş silindikten sonra hala mevcut. Dönen durum kodu: {res_get.status_code}"
