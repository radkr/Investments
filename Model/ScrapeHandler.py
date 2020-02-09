from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from Model.BaseHandler import BaseHandler


class ScrapeHandler(BaseHandler):

    browserUserCnt = 0
    browser = None

    def __init__(self, ticker, date_of_interest=None):
        super().__init__(ticker, date_of_interest)

        ScrapeHandler.browserUserCnt = ScrapeHandler.browserUserCnt + 1

    def __del__(self):
        ScrapeHandler.browserUserCnt = ScrapeHandler.browserUserCnt - 1
        if ScrapeHandler.browserUserCnt == 0:
            ScrapeHandler.stop_browser()

    @staticmethod
    def start_browser():

        if ScrapeHandler.browser is None:
            options = webdriver.ChromeOptions()

            options.add_experimental_option("prefs", {
                "download.default_directory": "/path/to/download/dir",
                "download.prompt_for_download": False,
            })

            options.add_argument('--headless')

            ScrapeHandler.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    @staticmethod
    def stop_browser():

        if ScrapeHandler.browser is not None:
            ScrapeHandler.browser.quit()

    @staticmethod
    def set_browser_download_path(path):

        if ScrapeHandler.browser is None:
            ScrapeHandler.start_browser()

        # add missing support for chrome "send_command"  to selenium webdriver
        ScrapeHandler.browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': path}}
        command_result = ScrapeHandler.browser.execute("send_command", params)

    @staticmethod
    def get_browser():

        if ScrapeHandler.browser is None:
            ScrapeHandler.start_browser()

        return ScrapeHandler.browser
