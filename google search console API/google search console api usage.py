import searchconsole
import os
from dotenv import load_dotenv
load_dotenv()
website = os.getenv("my_site")

account = searchconsole.authenticate(client_config='client_secrets.json')
webproperty = account[website]
report = webproperty.query.range('today', days= -14).dimension('query').get()
print(report.rows)


# Name = Md Kamruzzaman
# Submision_Date = 11/20/2022
# Assignment = Google Search Console Api Usage