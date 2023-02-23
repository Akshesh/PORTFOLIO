import scrapy

class PortfolioSpider(scrapy.Spider):
    name = 'portfolio'

    # The URLs to scrape
    start_urls = [
        'https://www.amplifypartners.com/portfolio',
        'https://lsvp.com/portfolio/'
    ]

    def parse(self, response):
        """
        Parses the HTML response and extracts the list of domains for all the portfolio companies.
        """
        domains = {}
        # Determine which website the response is for
        if response.url not in domains:
            domains[response.url] = []

        if 'amplifypartners.com' in response.url:
            companies = response.css('.companies-wr .w-dyn-item')
            for company in companies:
                status = company.css('div.status-div > div::text').get()
                if status and not any(status_word in status for status_word in ["Public", "Acquired"]):
                    company_name = company.css('.copy-wr > p::text').get().split()[0]
                    company_domain = company.css('div.website__link-wr > a::text').get()
                    domains[response.url].append({"company_domain": company_domain, "company_name": company_name })

        elif 'https://lsvp.com/portfolio' in response.url:
            companies = response.css('.portfolio-item')
            for company in companies:
                status = company.css('.subtitle::text').get()
                if status and not any(status_word in status for status_word in ["Public", "Acquired"]):
                    company_name = company.css('h2::text').get()
                    company_domain = company.css('.url::text').get()
                    domains[response.url].append({"company_domain": company_domain, "company_name": company_name })
        else:
            pass
        # Extract the list of domains for all the portfolio companies
        yield domains
