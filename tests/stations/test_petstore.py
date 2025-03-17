import time

import pytest
from fixtures.petstore.pet.model import Pet


class TestPet:

    @pytest.mark.positive
    def test_add_pet(self, app):
        """
        Test for adding a new pet.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Assert that the status code is 200 (or 201).
            4. Assert that the response contains the pet ID and name.
        """
        # 1. Yeni bir rastgele pet nesnesi oluştur
        data = Pet.random()

        # 2. Pet'i ekle
        res = app.pet_api.add_pet(data=data, type_response=Pet)

        # 3. Yanıtın başarılı olup olmadığını kontrol et
        assert res.status_code == 200  # veya 201
        assert isinstance(res.data, Pet), "Response data is not a Pet object"

        # 4. Dönen pet nesnesinin doğruluğunu kontrol et
        assert res.data.name == data.name, "Pet name mismatch"

    @pytest.mark.positive
    def test_get_pet_by_id(self, app):
        """
        Test for retrieving a pet by ID.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Retrieve the pet by its ID.
            4. Assert that the response status code is 200.
            5. Assert that the retrieved pet has the same ID and name.
        """
        # 1. Yeni bir rastgele pet nesnesi oluştur
        data = Pet.random()

        # 2. Pet'i ekle
        res_add = app.pet_api.add_pet(data=data, type_response=Pet)
        assert res_add.status_code == 200  # veya 201

        # 3. Pet'i ID ile getir
        res_get = app.pet_api.get_by_id_pet(pet_id=res_add.data.id, type_response=Pet)

        time.sleep(3)

        # 4. Yanıtın başarılı olup olmadığını kontrol et
        assert res_get.status_code == 200, "Get request failed"
        assert isinstance(res_get.data, Pet), "Response data is not a Pet object"

        # 5. Dönen pet nesnesinin doğruluğunu kontrol et
        assert res_get.data.name == data.name, "Pet name mismatch"

    @pytest.mark.positive
    def test_update_pet(self, app):
        """
        Test for updating a pet.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Update the pet.
            4. Assert that the update was successful.
        """
        # Yeni bir evcil hayvan oluştur
        new_pet = Pet.random()

        # Pet'i ekle
        created_pet = app.pet_api.add_pet(new_pet)
        assert created_pet.status_code == 200, "Failed to add pet"

        # Güncellenecek verileri hazırla
        updated_pet = created_pet.json()
        updated_pet["name"] = "UpdatedPetName"
        updated_pet["status"] = "sold"

        # Pet'i güncelle
        response = app.pet_api.update_pet(Pet(**updated_pet))
        assert response.status_code == 200, "Failed to update pet"
        updated_data = response.json()

        # Güncellenmiş verileri doğrula
        assert updated_data["id"] == created_pet.json()["id"]
        assert updated_data["name"] == "UpdatedPetName"
        assert updated_data["status"] == "sold"

    @pytest.mark.positive
    def test_delete_pet(self, app):
        """
        Test for deleting a pet.
        Steps:
            1. Create a new pet object.
            2. Add pet to the store.
            3. Delete the pet.
            4. Try to retrieve the pet by ID.
            5. Assert that the response status code for deletion is 200.
            6. Assert that retrieving the pet after deletion returns a 404.
        """
        # 1. Yeni bir pet nesnesi oluştur
        data = Pet.random()

        # 2. Pet'i ekle
        res_add = app.pet_api.add_pet(data=data, type_response=Pet)

        assert res_add.status_code == 200  # veya 201

        time.sleep(3)

        # 3. Pet'i sil
        res_delete = app.pet_api.delete_pet(pet_id=res_add.data.id)
        assert res_delete.status_code == 200, "Delete request failed"

        # Silme işlemi sonrasında yanıtın içeriğini yazdır
        print(f"Delete response: {res_delete.json()}")

        # 4. Silinen pet'in doğru şekilde silindiğinden emin ol
        res_get = app.pet_api.get_by_id_pet(pet_id=data.id, type_response=Pet)

        # Yanıtın doğru olup olmadığını kontrol et
        if res_get.status_code == 200:
            print(f"Pet exists after deletion, response: {res_get.json()}")

        # 5. Silinen pet'in hala mevcut olmaması ve 404 dönmesi gerektiğini doğrula
        assert (
            res_get.status_code == 404
        ), f"Pet still exists after deletion. Status code: {res_get.status_code}"
