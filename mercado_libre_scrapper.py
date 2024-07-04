import requests
from bs4 import BeautifulSoup

class MercadoLibreScrapper:
    URL = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/rm-metropolitana/providencia/_PriceRange_650000CLP-950000CLP_PublishedToday_YES_BEDROOMS_2-*_COVERED*AREA_80-*_FULL*BATHROOMS_2-*_NoIndex_True"

    def get_apartments_data_from_mercado_libre(self):
        search_results = self.get_search_results()
        apartments_data = []

        for result in search_results:
            apartments_data.append(
                {
                    "id": self.get_id(result),
                    "title": self.get_title(result),
                    "location": self.get_location(result),
                    "price": self.get_price(result),
                    "square_meters": self.get_square_meters(result),
                    "rooms_number": self.get_rooms_number(result),
                    "link": self.get_link(result)
                }
            )

        return apartments_data

    def get_search_results(self):
        page_source = requests.get(self.URL).text
        soup = BeautifulSoup(page_source, "html.parser")
        return soup.find_all("li", class_="ui-search-layout__item")

    def get_id(self, result):
        id_element = result.find("input", attrs={"name": "itemId"})
        return id_element.attrs["value"] if id_element else "Unknown ID"

    def get_title(self, result):
        title_element = result.find("h2", class_="ui-search-item__title")
        return title_element.string if title_element else "Unknown Title"

    def get_location(self, result):
        location_element = result.find("span", class_="ui-search-item__location-label")
        return location_element.string if location_element else "Unknown Location"

    def get_price(self, result):
        price_element = result.find("span", class_="andes-money-amount__fraction")
        return price_element.text.strip() if price_element else "Unknown Price"

    def get_square_meters(self, result):
        square_meters_elements = result.find_all("li", class_="ui-search-card-attributes__attribute")
        return square_meters_elements[0].string if square_meters_elements else "Unknown Square Meters"

    def get_rooms_number(self, result):
        rooms_number_elements = result.find_all("li", class_="ui-search-card-attributes__attribute")
        return rooms_number_elements[1].string if rooms_number_elements else "Unknown Rooms Number"

    def get_link(self, result):
        link_element = result.find("a", class_="ui-search-link")
        return link_element.attrs["href"] if link_element else "Unknown Link"
