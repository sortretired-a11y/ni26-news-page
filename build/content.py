"""Content of the 26 November 2026 page: every story, its badge and its pin.

Edit this file alone to change what the page says; render.py owns only layout.

Every item below is a Thursday 26 November 2026 event, or was first reported that
day somewhere in the world. Items that only look like today are named in the
DATE CHECK box instead of being counted.
"""

LEADS = [
    dict(tag="ASIA \u00b7 KOREA", src="KCNA",
         head="KIM ORDERS TACTICAL NUKES FIELDED WIDER",
         body="The North's leader calls for a broader deployment of short-range nuclear "
              "units and a faster build-up, days after a new solid-fuel test.",
         kind="rocket"),
    dict(tag="MIDEAST \u00b7 YEMEN", src="AL JAZEERA",
         head="BLAST ROCKS SANAA AS MISSILES CROSS TO RIYADH",
         body="An explosion hits the capital after strikes near the airport, and the Saudi "
              "coalition says it intercepted missiles over the kingdom's capital.",
         kind="tanker"),
    dict(tag="EUROPE \u00b7 UKRAINE", src="GENERAL STAFF",
         head="KYIV SAYS IT HIT A RUSSIAN AIR BASE AND FIVE PLANES",
         body="Ukrainian forces report damage to aircraft used to launch missiles and glide "
              "bombs, in one of the deepest strikes of the autumn.",
         kind="rubble"),
]

# (tag, headline, sub-line, drawn scene)
PANELS = [
    ("AMERICAS", "Storms push the Macy's parade to Saturday", "the 100th edition slips two days", "crown"),
    ("AMERICAS", "A king tide and El Nino surf batter California", "the Pacifica pier partly collapses", "warning"),
    ("ASIA", "Seoul's top court confirms Yoon's acquittal", "the last charge against him is closed", "gavel"),
    ("ASIA", "Seoul lifts its base rate to 3.25%", "the first rise in three years", "handshake"),
    ("ASIA", "A Hong Kong arts festival reports a data breach", "advance ticket buyers' details exposed", "shield"),

    ("MIDEAST", "Two Syrian security men die in an ISIL suicide attack", "the bomber struck a Damascus post", "rubble"),
    ("MIDEAST", "The UN warns of meningitis spreading in Gaza", "cases rising as displacement widens", "warning"),
    ("AFRICA", "Twelve killed in a road collision in Algeria", "fifteen more are being treated", "rubble"),
    ("OCEANIA", "Fiji declares a nationwide disaster as drought deepens", "92 communities are without water", "warning"),
    ("EUROPE", "Belgium says Iran likely ran fridge cyberattacks", "ministers split over the evidence", "shield"),
]

# (number, dateline, one line, outlet)
BRIEFS = [
    (16, "WASHINGTON", "Tariffs proposed on 14 partners, China and the EU among them", "AP"),
    (17, "NEW DELHI", "A 25% tariff on Indian goods, falling to 17% with a deal", "The Hindu"),
    (18, "KUALA LUMPUR", "Tariffs of up to 18% proposed on Malaysian goods", "NST"),
    (19, "TAIPEI", "Taiwan expects to keep the 15% rate it already agreed", "NST"),
    (20, "CANBERRA", "Parliament backs fines of up to 5% of global turnover", "NST"),
    (21, "SEOUL", "The central bank lifts its base rate 25bp to 3.25%", "NST"),
    (22, "BOGOR", "Thirteen confirmed dead, thirteen still trapped in the pit", "NST"),
    (23, "MANILA", "A strong quake brings a tsunami warning and emergency orders", "Paral"),
    (24, "ADEN", "Residents plan their escape as Houthis close on the city", "The Guardian"),
    (25, "DAMASCUS", "Two security personnel killed in an ISIL suicide bombing", "Al Jazeera"),
    (26, "GAZA CITY", "The UN warns of rising meningitis and new displacement", "Xinhua"),
    (27, "JERUSALEM", "Netanyahu says the corruption trial 'must end'", "Al Jazeera"),
    (28, "ALGIERS", "Twelve dead and fifteen hurt in a vehicle collision", "Xinhua"),
    (29, "SUVA", "A nationwide disaster is declared over the El Nino drought", "Paral"),
    (30, "BRUSSELS", "Ministers split over Iran's alleged fridge cyberattacks", "Reuters"),
    (31, "MOSCOW", "Europeans may join Ukraine talks if they 'contribute'", "Reuters"),
    (32, "BENGHAZI", "Libya vows retaliation for two officers lost to a sea drone", "AP"),
    (33, "BOGOTA", "Two police officers killed in a south-west armed attack", "Xinhua"),
    (34, "SINGAPORE", "The Think Asia Forum 2026 opens on regional cooperation", "Xinhua"),
    (35, "KIGALI", "African youth urged to shape the continent's future", "Xinhua"),
    (36, "MADRID", "A Salvadoran deported in error arrives in Spain", "AP"),
]

# One region per numbered item, in page order. Drives the masthead tally.
_LEAD_REGIONS = ["Asia East", "Mideast", "Europe"]
_PANEL_REGIONS = ["Americas", "Americas", "Asia East", "Asia East", "Asia East",
                  "Mideast", "Mideast", "Africa", "Oceania", "Europe"]
_BRIEF_REGIONS = ["Americas", "Asia South", "Asia East", "Asia East", "Oceania",
                  "Asia East", "Asia East", "Asia East", "Mideast", "Mideast",
                  "Mideast", "Mideast", "Africa", "Oceania", "Europe",
                  "Europe", "Africa", "Americas", "Asia East", "Africa", "Europe"]
_REGION_SEQ = _LEAD_REGIONS + _PANEL_REGIONS + _BRIEF_REGIONS

_TOTAL_ITEMS = len(LEADS) + len(PANELS) + len(BRIEFS)
assert len(_REGION_SEQ) == _TOTAL_ITEMS, (len(_REGION_SEQ), _TOTAL_ITEMS)

_tally = {}
for _r in _REGION_SEQ:
    _tally[_r] = _tally.get(_r, 0) + 1
REGIONS = sorted(_tally.items(), key=lambda kv: (-kv[1], kv[0]))
TOTAL = _TOTAL_ITEMS

PINS = {
    1: (39.0, 125.7), 2: (15.4, 44.2), 3: (51.5, 46.0),
    4: (40.7, -74.0), 5: (37.8, -122.4), 6: (37.6, 127.0), 7: (37.6, 127.0),
    8: (22.3, 114.2), 9: (33.5, 36.3), 10: (31.5, 34.5), 11: (36.8, 3.1),
    12: (-18.1, 178.4), 13: (50.8, 4.4),
    14: (38.9, -77.0), 15: (28.6, 77.2), 16: (3.1, 101.7), 17: (25.0, 121.5),
    18: (-35.3, 149.1), 19: (37.6, 127.0), 20: (-6.6, 106.8), 21: (14.6, 121.0),
    22: (12.8, 45.0), 23: (33.5, 36.3), 24: (31.5, 34.5), 25: (31.8, 35.2),
    26: (36.8, 3.1), 27: (-18.1, 178.4), 28: (50.8, 4.4), 29: (55.8, 37.6),
    30: (32.1, 20.1), 31: (4.7, -74.1), 32: (1.35, 103.8), 33: (-1.95, 30.06),
    34: (40.4, -3.7),
}

# Named on the page as deliberately left out: they read as today but are not.
EXCLUDED = ("Shenzhou-24 docking \u00b7 Canberra-Honiara treaty \u00b7 Cartagena siege "
            "\u00b7 Cairo tanker fire \u00b7 Poundland collapse \u00b7 Chen Jining inquiry "
            "\u00b7 Dhaka garment wage")

# The strip under the leads.
NUMBERS = [
    ("25%", "proposed US tariff on Indian goods"),
    ("3.25%", "Korea's base rate, up 25bp"),
    ("13", "confirmed dead in the West Java mine"),
    ("18%", "proposed tariff on Malaysian goods"),
    ("5%", "of global turnover, Australia's new fine cap"),
    ("15%", "the tariff rate Taiwan expects to keep"),
]

KICKER = ("Kim orders tactical nukes fielded wider \u00b7 Blast rocks Sanaa as missiles "
          "cross to Riyadh \u00b7 Kyiv says it hit a Russian air base and five planes")
