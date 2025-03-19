from requests import Response

from fixtures.petstore.store.model import Order
from fixtures.validator import Validator


class StoreAPI(Validator):

    def __init__(self, app):
        """
        StoreAPI sınıfı, mağaza ile ilgili API işlemleri için yardımcı metotları içerir.
        :param app: Uygulama nesnesi, API isteği yapmak için client'ı sağlar.
        """
        self.app = app

    POST_ORDER = "/store/order"  # Sipariş eklemek için kullanılan endpoint
    GET_ORDER = "/store/order/{}"  # Sipariş almak için kullanılan endpoint
    DELETE_ORDER = "/store/order/{}"  # Sipariş silmek için kullanılan endpoint

    def add_order(self, data: Order, type_response=Order) -> Response:
        """
        Yeni bir sipariş ekler.
        :param data: Order modelinden bir nesne. Bu, eklenecek siparişin verilerini içerir.
        :param type_response: (opsiyonel) Dönen yanıtı hangi tipe dönüştürmek istediğinizi belirler (varsayılan olarak Order).
        :return: API'nin döndürdüğü yanıt (Response nesnesi).
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_ORDER}",
            json=data.to_dict(),
        )
        return self.structure(response, type_response=type_response)

    def get_order_by_id(self, order_id: int, type_response=Order) -> Response:
        """
        Verilen ID ile bir siparişi alır.
        :param order_id: Siparişin benzersiz kimliği (ID).
        :param type_response: (opsiyonel) Dönen yanıtı hangi tipe dönüştürmek istediğinizi belirler (varsayılan olarak Order).
        :return: Siparişin bilgilerini içeren yanıt.
        """
        response = self.app.client.request(
            method="GET",
            url=f"{self.app.url}{self.GET_ORDER.format(order_id)}",
        )
        return self.structure(response, type_response=type_response)

    def delete_order(self, order_id: int) -> Response:
        """
        Belirli bir siparişi sipariş ID'sine göre siler.
        :param order_id: Silinecek siparişin benzersiz kimliği (ID).
        :return: API'nin döndürdüğü yanıt (Response nesnesi).
        """
        response = self.app.client.request(
            method="DELETE",
            url=f"{self.app.url}{self.DELETE_ORDER.format(order_id)}",
        )
        return response
