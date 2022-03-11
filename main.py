import requests_html
import pandas as pd
import openpyxl



def links_scraper():
    tables = r.html.find("table tbody tr th")
    for i in tables:
        if i.text == "":
            link_list.append(i.find("a")[0].attrs["href"])



def scraper(no, lidz):
    for i in range (no, lidz):
        try:
            pok_data = []
            pok_link=(link_list[i])
            pok_URL = f"https://bulbapedia.bulbagarden.net{pok_link}"
            pok_r = session.get(pok_URL)
            pok1 = pok_r.html.find(".roundy tbody tr td table tbody")[0]
            pok_data.append(pok1.find("th big big span")[0].text) #ID
            pok_data.append(pok1.find("tr big big b")[0].text) #Name
            pok2 = pok_r.html.find(".roundy tbody tr td table tbody")[3]
            pok_data.append(pok2.find("tr td table tbody td")[0].text) #Type 1
            pok_data.append(pok2.find("tr td table tbody td")[1].text) #Type 2
            pok_data.append(pok_r.html.find("div.mw-parser-output table tbody tr th div")[1].text) #HP
            pok_data.append(pok_r.html.find("div.mw-parser-output table tbody tr th div")[3].text) #attack
            pok_data.append(pok_r.html.find("div.mw-parser-output table tbody tr th div")[5].text) #deffence
            pok_data.append(pok_r.html.find("div.mw-parser-output table tbody tr th div")[7].text) #special attack
            pok_data.append(pok_r.html.find("div.mw-parser-output table tbody tr th div")[9].text) #special deffence
            pok_data.append(pok_r.html.find("div.mw-parser-output table tbody tr th div")[11].text) #speed

            pok_list.append(pok_data)
        except:
            pass


def pok_power_df():
    for i in range(len(df.index)):
        power = 0
        for j in range(len(df.index) - 1):
            power = power + (int(df.iat[i, 5]) - int(df.iat[j, 6])) * 0.8 + (int(df.iat[i, 7]) - int(df.iat[j, 8]) * 0.2)
            df.iat[i, 10] = power
    power_table = df.sort_values(by='Power', ascending=False)
    final_table = power_table.drop_duplicates()

    with pd.ExcelWriter("final_table.xlsx") as writer:
        final_table.to_excel(writer)

    return print(final_table)

if __name__ == '__main__':
    try:
        output = pd.read_pickle("pok_file.pkl")
        print("opening file")
        df = pd.DataFrame(output)
        df["Power"] = 0
        print ("create power tableed")
        pok_power_df()
        print("table print")



    except:
        print("Let's start scraping")
        session = requests_html.HTMLSession()
        URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
        r = session.get(URL)
        link_list = []
        pok_list = []
        links_scraper()
        scraper(0, len(link_list))
        df = pd.DataFrame(pok_list,
                          columns=["ID", "Name", "Type1", "Type2", "HP", "Atk", "Def", "Sp_Atk", "Sp_Def", "Speed"])
        df.to_pickle("pok_file.pkl")
        df["Power"] = 0
        pok_power_df()

