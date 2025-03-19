from requests import Response
from fixtures.petstore.user.model import User
from fixtures.validator import Validator


class UserAPI(Validator):

    def __init__(self, app):
        """
        UserAPI sınıfı, kullanıcı ile ilgili API işlemleri için yardımcı metotları içerir.
        :param app: Uygulama nesnesi, API isteği yapmak için client'ı sağlar.
        """
        self.app = app

    POST_USER = "/user"  # Kullanıcı eklemek için kullanılan endpoint
    GET_USER = "/user/{}"  # Kullanıcı almak için kullanılan endpoint
    PUT_USER = "/user/{}"  # Kullanıcı güncellemek için kullanılan endpoint
    DELETE_USER = "/user/{}"  # Kullanıcı silmek için kullanılan endpoint
    LOGIN_USER = "/user/login"  # Kullanıcı giriş endpointi
    LOGOUT_USER = "/user/logout"  # Kullanıcı çıkış endpointi

    def add_user(self, data: User, type_response=User) -> Response:
        """
        Yeni bir kullanıcı ekler.
        :param data: User modelinden bir nesne. Bu, eklenecek kullanıcının verilerini içerir.
        :param type_response: (opsiyonel) Dönen yanıtı hangi tipe dönüştürmek istediğinizi belirler (varsayılan olarak User).
        :return: API'nin döndürdüğü yanıt (Response nesnesi).
        """
        response = self.app.client.request(
            method="POST",
            url=f"{self.app.url}{self.POST_USER}",
            json=data.to_dict(),
        )
        return self.structure(response, type_response=type_response)

    def get_user_by_username(self, username: str, type_response=User) -> Response:
        """
        Verilen kullanıcı adı ile bir kullanıcıyı alır.
        :param username: Kullanıcının benzersiz adı.
        :param type_response: (opsiyonel) Dönen yanıtı hangi tipe dönüştürmek istediğinizi belirler (varsayılan olarak User).
        :return: Kullanıcı bilgilerini içeren yanıt.
        """
        response = self.app.client.request(
            method="GET",
            url=f"{self.app.url}{self.GET_USER.format(username)}",
        )
        return self.structure(response, type_response=type_response)

    def update_user(self, data: User, type_response=User) -> Response:
        """
        Belirli bir kullanıcının bilgilerini günceller.
        :param username: Güncellenecek kullanıcının adı.
        :param data: Güncellenmiş kullanıcı bilgilerini içeren User nesnesi.
        :param type_response: (opsiyonel) Dönen yanıtı hangi tipe dönüştürmek istediğinizi belirler.
        :return: API'nin döndürdüğü yanıt (Response nesnesi).
        """
        response = self.app.client.request(
            method="PUT",
            url=f"{self.app.url}{self.PUT_USER.format(data.username)}",
            json=data.to_dict(),
        )
        return self.structure(response, type_response=type_response)

    def delete_user(self, username: str) -> Response:
        """
        Belirli bir kullanıcıyı kullanıcı adına göre siler.
        :param username: Silinecek kullanıcının adı.
        :return: API'nin döndürdüğü yanıt (Response nesnesi).
        """
        response = self.app.client.request(
            method="DELETE",
            url=f"{self.app.url}{self.DELETE_USER.format(username)}",
        )
        return response

    def login(self, username: str, password: str) -> Response:
        """
        Kullanıcıyı kullanıcı adı ve şifre ile giriş yapar.
        :param username: Kullanıcının kullanıcı adı.
        :param password: Kullanıcının şifresi.
        :return: API yanıtı (Response nesnesi) içerir.
        """
        response = self.app.client.request(
            method="GET",  # Assuming GET method for login
            url=f"{self.app.url}{self.LOGIN_USER}",
            params={
                "username": username,
                "password": password,
            },  # Using query parameters for GET
        )
        return response

    def logout(self) -> Response:
        """
        Mevcut kullanıcıyı çıkış yapar.
        :return: API yanıtı (Response nesnesi) içerir.
        """
        response = self.app.client.request(
            method="GET",  # Assuming GET method for logout
            url=f"{self.app.url}{self.LOGOUT_USER}",
        )
        return response
