# controllers/inject_controller.py

class InjectController:
    def __init__(self, browser):
        self.browser = browser

    def inject(self, base_url: str, payload: str):
        if not base_url or not payload:
            return

        final_url = base_url + payload
        self.browser.setUrl(final_url)
