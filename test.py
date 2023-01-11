import requests
import pandas as pd
import json
import csv

# codes = (
#     pd.read_csv(
#         "https://gist.githubusercontent.com/ilyankou/b2580c632bdea4af2309dcaa69860013/raw/420fb417bcd17d833156efdf64ce8a1c3ceb2691/country-codes",
#         dtype=str,
#     )
#     .fillna("NA")
#     .set_index("ISO2")
# )

codes = {}
with open("code.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        codes[row["ISO2"]] = row["Country"]

# iso2name = {x: y["Country"] for x, y in codes.iterrows()}


def fix_iso2(x):
    o = {"UK": "GB", "RK": "XK"}
    return o[x] if x in o else x


def reverse_iso2(x):
    o = {"GB": "UK", "XK": "RK"}
    return o[x] if x in o else x


# x = [
#     "AD",
#     "AE",
#     "AF",
#     "AG",
#     "AL",
#     "AM",
#     "AO",
#     "AR",
#     "AT",
#     "AU",
#     "AZ",
#     "BA",
#     "BB",
#     "BD",
#     "BE",
#     "BF",
#     "BG",
#     "BH",
#     "BI",
#     "BJ",
#     "BN",
#     "BO",
#     "BR",
#     "BS",
#     "BT",
#     "BW",
#     "BY",
#     "BZ",
#     "CA",
#     "CD",
#     "CF",
#     "CG",
#     "CH",
#     "CI",
#     "CL",
#     "CM",
#     "CN",
#     "CO",
#     "CR",
#     "CU",
#     "CV",
#     "CY",
#     "CZ",
#     "DE",
#     "DJ",
#     "DK",
#     "DM",
#     "DO",
#     "DZ",
#     "EC",
#     "EE",
#     "EG",
#     "ER",
#     "ES",
#     "ET",
#     "FI",
#     "FJ",
#     "FM",
#     "FR",
#     "GA",
#     "GB",
#     "GD",
#     "GE",
#     "GH",
#     "GM",
#     "GN",
#     "GQ",
#     "GR",
#     "GT",
#     "GW",
#     "GY",
#     "HK",
#     "HN",
#     "HR",
#     "HT",
#     "HU",
#     "ID",
#     "IE",
#     "IL",
#     "IN",
#     "IQ",
#     "IR",
#     "IS",
#     "IT",
#     "JM",
#     "JO",
#     "JP",
#     "KE",
#     "KG",
#     "KH",
#     "KI",
#     "KM",
#     "KN",
#     "KP",
#     "KR",
#     "KW",
#     "KZ",
#     "LA",
#     "LB",
#     "LC",
#     "LI",
#     "LK",
#     "LR",
#     "LS",
#     "LT",
#     "LU",
#     "LV",
#     "LY",
#     "MA",
#     "MC",
#     "MD",
#     "ME",
#     "MG",
#     "MH",
#     "MK",
#     "ML",
#     "MM",
#     "MN",
#     "MO",
#     "MR",
#     "MT",
#     "MU",
#     "MV",
#     "MW",
#     "MX",
#     "MY",
#     "MZ",
#     "NA",
#     "NE",
#     "NG",
#     "NI",
#     "NL",
#     "NO",
#     "NP",
#     "NR",
#     "NZ",
#     "OM",
#     "PA",
#     "PE",
#     "PG",
#     "PH",
#     "PK",
#     "PL",
#     "PS",
#     "PT",
#     "PW",
#     "PY",
#     "QA",
#     "RO",
#     "RS",
#     "RU",
#     "RW",
#     "SA",
#     "SB",
#     "SC",
#     "SD",
#     "SE",
#     "SG",
#     "SI",
#     "SK",
#     "SL",
#     "SM",
#     "SN",
#     "SO",
#     "SR",
#     "SS",
#     "ST",
#     "SV",
#     "SY",
#     "SZ",
#     "TD",
#     "TG",
#     "TH",
#     "TJ",
#     "TL",
#     "TM",
#     "TN",
#     "TO",
#     "TR",
#     "TT",
#     "TV",
#     "TW",
#     "TZ",
#     "UA",
#     "UG",
#     "US",
#     "UY",
#     "UZ",
#     "VA",
#     "VC",
#     "VE",
#     "VN",
#     "VU",
#     "WS",
#     "XK",
#     "YE",
#     "ZA",
#     "ZM",
#     "ZW",
# ]

# for region in x:
#     result_raw = requests.get(
#         f"https://api.henleypassportindex.com/api/passports/{region}/countries",
#         headers={
#             "User-Agent": "Mozilla/5.0",
#             "Accept": "*/*",
#             "Accept-Language": "en-US,en;q=0.5",
#             "Accept-Encoding": "gzip, deflate, br",
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "Pragma": "no-cache",
#             "Cache-Control": "no-cache",
#         },
#     )
#     print(result_raw)
#     with open(f"HPI-{region}.json", "w") as file:
#         file.write(result_raw.text)

dataHPI = {}
for region in codes:
    with open(f"HPI-{region}.json", "r") as f:
        data = json.load(f)
        dataHPI[region] = {}
        for destination in data["default"]:
            # if destination["pivot"]["is_visa_free"] == 1:
            #     if destination["pivot"]["visa_access_id"] not in [1, 4, 5]:
            #         print(destination["code"], destination["pivot"]["visa_access_id"])
            if destination["pivot"]["is_visa_free"] != 1:
                dataHPI[region][destination["code"]] = "visa required"
            elif destination["pivot"]["visa_access_id"] == 1:
                dataHPI[region][destination["code"]] = "visa free"
            elif destination["pivot"]["visa_access_id"] == 4:
                dataHPI[region][destination["code"]] = "visa on arrival"
            elif destination["pivot"]["visa_access_id"] == 5:
                dataHPI[region][destination["code"]] = "e-visa"
            else:
                print("error!!!")

# print(dataHPI)

import csv

dataPI = {}
with open("passport-index-matrix-iso2.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        dataPI[row["Passport"]] = {}
        for destination in row:
            dataPI[row["Passport"]][destination] = row[destination]

# print(dataPI)

# Compare the two datasets and print the differences:
print(
    "Passport,Destination,PI,HPI",
)

for passport in dataPI:
    for destination in dataPI[passport]:
        if passport != "Passport" and destination != "Passport":
            if dataPI[passport][destination] != dataHPI[passport][destination]:
                if not (
                    dataHPI[passport][destination] == "visa free"
                    and dataPI[passport][destination].isnumeric()
                ):
                    if not dataPI[passport][destination] == "-1":
                        print(
                            f"{codes[passport]},{codes[destination]},{dataPI[passport][destination]},{dataHPI[passport][destination]}"
                        )

# with open("HPI.csv", "w") as f:
#     f.write(dataHPI)
json.dump(dataHPI, open("HPI.json", "w"))
