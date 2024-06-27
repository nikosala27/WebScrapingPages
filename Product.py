class Product():
    def __init__(self, name: str = "", price: float = 0.0, url: str = "", code: str = "", category: str = "") -> None:
        self.name = name
        self.price = price
        self.url = url
        self.code = code
        self.category = category

    def __str__(self) -> str:
        product_str = f"Nazwa produktu: {self.name}, Cena produktu: {self.price}, Kod produktu: {self.code}, Kategoria: {self.category}, Link: {self.url}"
        return product_str
