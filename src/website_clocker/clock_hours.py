class WebsiteClocker:
    def __init__(self, url):
        self.url = url

    def clock_hours(self):
        import requests
        
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                print(f"Successfully clocked hours at {self.url}")
            else:
                print(f"Failed to clock hours. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    clocker = WebsiteClocker("http://example.com")
    clocker.clock_hours()