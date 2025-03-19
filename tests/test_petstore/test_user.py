import time

import pytest
from fixtures.petstore.user.model import User


class TestUser:

    @pytest.mark.positive
    def test_add_user(self, app):
        """
        Test for adding a new user.
        """
        data = User.random()
        res = app.user_api.add_user(data=data)

        time.sleep(5)

        assert res.status_code == 200
        assert isinstance(res.data, User), "Response data is not a User object"
        assert res.data.username == data.username, "Username mismatch"

    @pytest.mark.positive
    def test_get_user_by_username(self, app):
        """
        Test for retrieving a user by username.
        """
        data = User.random()
        res_add = app.user_api.add_user(data=data)
        assert res_add.status_code == 200

        time.sleep(5)

        res_get = app.user_api.get_user_by_username(username=data.username)
        assert res_get.status_code == 200, "Get request failed"
        assert res_get.data.username == data.username, "Username mismatch"

    @pytest.mark.positive
    def test_update_user(self, app):
        """
        Kullanıcı güncelleme işlemini test eder.
        """

        # 1. Yeni bir kullanıcı oluştur
        data = User.random()  # Rastgele kullanıcı oluştur
        created_user = app.user_api.add_user(data)
        assert created_user.status_code == 200, "Kullanıcı oluşturulamadı"

        # 2. Kullanıcıyı güncellemeden önceki veriyi al ve değiştir
        updated_user = created_user.data.to_dict()  # Mevcut kullanıcı bilgilerini al
        updated_user["firstName"] = "UpdatedFirstName"
        updated_user["lastName"] = "UpdatedLastName"

        # 3. Güncelleme işlemini gerçekleştir
        response = app.user_api.update_user(User(**updated_user))
        assert response.status_code == 200, "Kullanıcı güncellenemedi"

        # 4. API'den güncellenmiş kullanıcı bilgilerini al
        res_get = app.user_api.get_user_by_username(username=updated_user["username"])
        assert res_get.status_code == 200, "Güncellenmiş kullanıcı bilgileri alınamadı"

        # 5. Güncellenmiş bilgileri doğrula
        get_user_data = res_get.data.to_dict()
        assert (
            get_user_data["firstName"] == "UpdatedFirstName"
        ), f"Beklenen UpdatedFirstName ancak {get_user_data['firstName']} alındı"
        assert (
            get_user_data["lastName"] == "UpdatedLastName"
        ), f"Beklenen UpdatedLastName ancak {get_user_data['lastName']} alındı"

    @pytest.mark.positive
    def test_delete_user(self, app):
        """
        Test for deleting a user.
        """
        data = User.random()
        res_add = app.user_api.add_user(data=data, type_response=User)
        assert res_add.status_code == 200

        time.sleep(5)

        res_delete = app.user_api.delete_user(username=data.username)
        assert res_delete.status_code == 200, "Delete request failed"

    @pytest.mark.positive
    def test_user_login(self, app):
        """
        Test for user login.
        """
        data = User.random()
        res_add = app.user_api.add_user(data=data, type_response=User)
        assert res_add.status_code == 200

        time.sleep(5)

        res_login = app.user_api.login(username=data.username, password=data.password)
        assert res_login.status_code == 200, "Login request failed"

    @pytest.mark.positive
    def test_user_logout(self, app):
        """
        Test for user logout.
        """
        res_logout = app.user_api.logout()
        assert res_logout.status_code == 200, "Logout request failed"
