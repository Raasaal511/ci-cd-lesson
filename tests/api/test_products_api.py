import pytest


@pytest.fixture
def product(client, catalog_id):
    response = client.post(
        "/products",
        json={"name": "Ноутбук", "price": 1500.5, "quantity": 2, "catalog_id": catalog_id},
    )
    return response.json()


def test_create_product(client, catalog_id):
    response = client.post(
        "/products",
        json={
            "name": "Смартфон",
            "description": "128 ГБ",
            "price": 799.99,
            "quantity": 10,
            "catalog_id": catalog_id,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Смартфон",
        "description": "128 ГБ",
        "price": 799.99,
        "quantity": 10,
        "in_stock": True,
        "catalog_id": catalog_id,
    }


def test_create_product_defaults(client, catalog_id):
    body = client.post(
        "/products", json={"name": "Кабель", "price": 5, "catalog_id": catalog_id}
    ).json()

    assert body["quantity"] == 0
    assert body["in_stock"] is False
    assert body["description"] is None


def test_create_product_in_missing_catalog_returns_404(client):
    response = client.post("/products", json={"name": "Товар", "price": 1, "catalog_id": 999})

    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Товар", "price": -1},
        {"name": "Товар", "price": 1, "quantity": -1},
        {"name": "", "price": 1},
        {"price": 1},
        {"name": "Товар", "price": "дорого"},
    ],
)
def test_create_product_validation(client, catalog_id, payload):
    response = client.post("/products", json={**payload, "catalog_id": catalog_id})

    assert response.status_code == 422


def test_get_product(client, product):
    response = client.get(f"/products/{product['id']}")

    assert response.status_code == 200
    assert response.json() == product


def test_get_missing_product_returns_404(client):
    assert client.get("/products/999").status_code == 404


def test_list_products_with_filter(client, catalog_id):
    other = client.post("/catalogs", json={"name": "Кухня"}).json()["id"]
    client.post("/products", json={"name": "Ноутбук", "price": 1, "catalog_id": catalog_id})
    client.post("/products", json={"name": "Чайник", "price": 1, "catalog_id": other})

    all_products = client.get("/products").json()
    kitchen = client.get("/products", params={"catalog_id": other}).json()

    assert len(all_products) == 2
    assert [p["name"] for p in kitchen] == ["Чайник"]


def test_update_product(client, product):
    response = client.patch(f"/products/{product['id']}", json={"price": 1200, "quantity": 0})

    assert response.status_code == 200
    body = response.json()
    assert body["price"] == 1200
    assert body["quantity"] == 0
    assert body["in_stock"] is False
    assert body["name"] == product["name"]


def test_update_product_to_missing_catalog_returns_404(client, product):
    response = client.patch(f"/products/{product['id']}", json={"catalog_id": 999})

    assert response.status_code == 404


def test_update_product_null_price_returns_422(client, product):
    assert client.patch(f"/products/{product['id']}", json={"price": None}).status_code == 422


def test_delete_product(client, product):
    assert client.delete(f"/products/{product['id']}").status_code == 204
    assert client.get(f"/products/{product['id']}").status_code == 404


def test_deleting_catalog_deletes_its_products(client, catalog_id, product):
    client.delete(f"/catalogs/{catalog_id}")

    assert client.get(f"/products/{product['id']}").status_code == 404
