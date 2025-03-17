from requests import Response

from fixtures.petstore.pet.model import Pet
from fixtures.validator import Validator


class PetAPI(Validator):

    def __init__(self, app):
        """
        PetAPI sınıfı, pet ile ilgili API işlemleri için yardımcı metotları içerir.
        :param app: Uygulama nesnesi, API isteği yapmak için client'ı sağlar.
        """
        self.app = app

    POST_PET = "/pet"  # Pet eklemek için kullanılan endpoint
    GET_PET = "/pet/{}"  # Pet almak için kullanılan endpoint
    PUT_PET = "/pet"  # Pet güncellemek için kullanılan endpoint
    DELETE_PET = "/pet/{}"  # Pet silmek için kullanılan endpoint

    def add_pet(self, data: Pet, type_response=Pet) -> Response:
        """
        Yeni bir pet ekler.
        :param data: Pet modelinden bir nesne. Bu, eklenecek pet'in verilerini içerir.
        :param type_response: (opsiyonel) Dönen yanıtı hangi tipe dönüştürmek istediğinizi belirler (varsayılan olarak Pet).
        :return: API'nin döndürdüğü yanıt (Response nesnesi).
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_PET}",
            json=data.to_dict(),  # Pet verisini JSON formatında gönder
        )
        return self.structure(
            response, type_response=type_response
        )  # Yanıtı yapılandırır

    def get_by_id_pet(self, pet_id: int, type_response=Pet) -> Response:
        """
        Verilen ID ile bir pet'i alır.
        :param pet_id: Pet'in benzersiz kimliği (ID).
        :param type_response: (opsiyonel) Dönen yanıtı hangi tipe dönüştürmek istediğinizi belirler (varsayılan olarak Pet).
        :return: Pet'in bilgilerini içeren yanıt.
        """
        response = self.app.client.request(
            method="GET",
            url=f"{self.app.url}{self.GET_PET.format(pet_id)}",  # Pet ID'si URL'ye eklenir
        )
        return self.structure(
            response, type_response=type_response
        )  # Yanıtı yapılandırır

    def update_pet(self, data: Pet, type_response=Pet) -> Response:
        """
        Mevcut bir pet'i günceller.
        :param data: Pet modelinden bir nesne. Bu, güncellenmiş pet verilerini içerir.
        :param type_response: (opsiyonel) Dönen yanıtı hangi tipe dönüştürmek istediğinizi belirler (varsayılan olarak Pet).
        :return: API'nin döndürdüğü yanıt (Response nesnesi).
        """
        response = self.app.client.request(
            method="PUT",
            url=f"{self.app.url}{self.PUT_PET}",
            json=data.to_dict(),  # Güncellenmiş pet verilerini JSON formatında gönder
        )
        return self.structure(
            response, type_response=type_response
        )  # Yanıtı yapılandırır

    def delete_pet(self, pet_id: int) -> Response:
        """
        Belirli bir pet'i pet ID'sine göre siler.
        :param pet_id: Silinecek pet'in benzersiz kimliği (ID).
        :return: API'nin döndürdüğü yanıt (Response nesnesi).
        """
        response = self.app.client.request(
            method="DELETE",
            url=f"{self.app.url}{self.DELETE_PET.format(pet_id)}",  # Pet ID'si URL'ye eklenir
        )
        return response  # Silme işlemiyle ilgili yanıtı geri döndürür
