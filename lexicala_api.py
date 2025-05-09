import requests

class LexicalaAPI:
    def __init__(self):
        self.api_key = "57e1cbd235msh7af6ea007827d41p10aa13jsn7772d6aab5ef"
        self.base_url = "https://api.lexicala.com"

    def search_word(self, word, lang="en"):
        url = f"{self.base_url}/search?text={word}&language={lang}"
        headers = {
            "x-rapidapi-host": "lexicala1.p.rapidapi.com",
            "x-rapidapi-key": "57e1cbd235msh7af6ea007827d41p10aa13jsn7772d6aab5ef"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print("Request failed:", response.status_code)

    # def get_entry(self, entry_id, lang="en"):
    #     url = f"{self.base_url}/entries/{entry_id}?language={lang}"
    #     headers = {"Authorization": f"Bearer {self.api_key}"}
    #     response = requests.get(url, headers=headers)

    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         print("❌ Entry fetch error:", response.status_code)
    #         return None
