def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_catalog(client):
    response = client.post("/catalogs", json={"name": "Книги", "description": "Всё о книгах"})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "Книги", "description": "Всё о книгах"}


def test_create_catalog_duplicate_returns_409(client):
    client.post("/catalogs", json={"name": "Книги"})
    response = client.post("/catalogs", json={"name": "Книги"})

    assert response.status_code == 409


def test_create_catalog_validation(client):
    assert client.post("/catalogs", json={"name": ""}).status_code == 422
    assert client.post("/catalogs", json={}).status_code == 422
    # Только пробелы проходят схему, но отклоняются доменной сущностью.
    assert client.post("/catalogs", json={"name": "   "}).status_code == 422


def test_list_catalogs(client):
    for name in ("A", "B", "C"):
        client.post("/catalogs", json={"name": name})

    response = client.get("/catalogs", params={"offset": 1, "limit": 1})

    assert response.status_code == 200
    assert [c["name"] for c in response.json()] == ["B"]


def test_get_catalog(client, catalog_id):
    response = client.get(f"/catalogs/{catalog_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Электроника"


def test_get_missing_catalog_returns_404(client):
    response = client.get("/catalogs/999")

    assert response.status_code == 404
    assert "не найден" in response.json()["detail"]


def test_update_catalog_partially(client):
    created = client.post("/catalogs", json={"name": "Старое", "description": "desc"}).json()

    response = client.patch(f"/catalogs/{created['id']}", json={"name": "Новое"})

    assert response.status_code == 200
    assert response.json() == {"id": created["id"], "name": "Новое", "description": "desc"}


def test_update_catalog_null_name_returns_422(client, catalog_id):
    assert client.patch(f"/catalogs/{catalog_id}", json={"name": None}).status_code == 422


def test_delete_catalog(client, catalog_id):
    assert client.delete(f"/catalogs/{catalog_id}").status_code == 204
    assert client.get(f"/catalogs/{catalog_id}").status_code == 404
    assert client.delete(f"/catalogs/{catalog_id}").status_code == 404


def test_list_catalog_products(client, catalog_id):
    other = client.post("/catalogs", json={"name": "Другой"}).json()["id"]
    client.post("/products", json={"name": "Ноутбук", "price": 1000, "catalog_id": catalog_id})
    client.post("/products", json={"name": "Чайник", "price": 20, "catalog_id": other})

    response = client.get(f"/catalogs/{catalog_id}/products")

    assert response.status_code == 200
    assert [p["name"] for p in response.json()] == ["Ноутбук"]


def test_list_products_of_missing_catalog_returns_404(client):
    assert client.get("/catalogs/999/products").status_code == 404
