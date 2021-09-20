from selenium import webdriver

from file_writer import FileWriter


DESIRED_SECTIONS = ["processo", "órgão julgador", "data do julgamento", "data da publicação"]
WEBDRIVER_PATH = "/usr/local/bin/chromedriver"
BINARY_PATH = "/usr/bin/google-chrome"


class Stj:
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=WEBDRIVER_PATH)
        self.outputs = []
        
    def enter(self):
        self.browser.get("https://scon.stj.jus.br/SCON/")

    def show_form(self):
        advanced_search_btn = self.browser.find_element_by_id("idMostrarPesquisaAvancada")
        advanced_search_btn.click()

    def fill_form(self):
        start_date = self.browser.find_element_by_id("data_inicial")
        end_date = self.browser.find_element_by_id("data_final")

        start_date.send_keys("01/09/2021")
        end_date.send_keys("02/09/2021")

    def search(self):
        form_btns = self.browser.find_element_by_class_name("botoesForm")
        search_btns = form_btns.find_elements_by_tag_name("input")

        for search_btn in search_btns:
            if search_btn.get_attribute("value") == "Pesquisar":
                search_btn.click()
                break
    
    def _get_section_infos(self, section):
        section_title = section.find_element_by_class_name("docTitulo")
        section_title_text = section_title.text.lower()

        section_content = section.find_element_by_class_name("docTexto")
        return section_title_text, section_content.text

    def _must_scrape_section(self, section_title):
        for desired_section in DESIRED_SECTIONS:
            if section_title in desired_section:
                return True
        return False

    @property
    def documents(self):
        return self.outputs

    def get_documents(self):
        documents = self.browser.find_elements_by_class_name("documento")

        for document in documents:
            output = {}
            sections = document.find_elements_by_class_name("paragrafoBRS")
            for section in sections:
                section_title, section_content = self._get_section_infos(section)
                must_scrape = self._must_scrape_section(section_title)

                if must_scrape:
                    output[section_title] = section_content
                    self.outputs.append(output)

    def next_page(self):
        next_page_btn = self.browser.find_element_by_class_name("iconeProximaPagina")
        next_page_btn.click()

stj = Stj()
stj.enter()
stj.show_form()
stj.fill_form()
stj.search()

while True:
    stj.get_documents()
    stj.next_page()
    file_writer = FileWriter()
    file_writer.save(stj.documents)