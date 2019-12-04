import dash_html_components as html

def get_current_version() -> str:
    with open("VERSION") as f:
        v = f.readline().replace("\n", "")
    return v

def get_sidecart(context: str = "mortality") -> list:
    sidecart_texts = {
        "mortality": "This plot shows cumulative morbidity (number of cases) and mortality (number of deaths) from "
                     "measles associated causes.",
        "age_group": "This plot shows morbidity (number of cases) and mortality (number of deaths) by age group.",
        "cfr": "CFR, or case-fatality ratio, shows the relative mortality in relation to morbidity – in other words, "
               "how many patients afflicted succumb to the disease in the short term."
    }

    sidecart_help: list = [
        html.Hr(),
        html.P(["Last update: ",
                html.Span([""], id="last-update")]),
        html.Hr(),
        html.H4("How you can help"),
        html.P(["The Government of Samoa has established a ",
                html.A("direct donation fund",
                       href="https://twitter.com/samoagovt/status/1199517609621774336",
                       target="_blank"), " "
                "through which you can contribute to relief efforts. ",
                html.A("UNICEF NZ",
                       href="https://www.unicef.org.nz/appeal/samoa-measles-emergency",
                       target="_blank"), " "
                "is also running an emergency appeal for the measles crisis in Samoa.", " ",
                "Furthermore, a private fundraiser by ", html.A("@MsTrixter", href="https://twitter.com/MsTrixter"), " ",
                "has also been set up on", html.A("GoFundMe", href="https://www.gofundme.com/f/samoa-measles-outbreak"), "."])
    ]

    sidecart_data_source: list = [
        html.H4("Data source"),
        html.P(["Data has been parsed from the periodic reports of the Government of Samoa. The data is available to ",
                "all interested parties ",
                html.A("on Github", href="https://github.com/chrisvoncsefalvay/samoa-measles-2019")], "."),
        html.P(["To cite this document, you may use the following citation: ",
                html.A(children=[
                    html.Img(src="https://zenodo.org/badge/225143525.svg")
                ], href="https://zenodo.org/badge/latestdoi/225143525")]),
        html.Hr(),
        html.P(["(c)", " ", html.A("Chris von Csefalvay", href="https://chrisvoncsefalvay.com"), " ", "2019."]),
        html.P(["App version: ", get_current_version()])
    ]

    return [sidecart_texts[context]] + sidecart_help + sidecart_data_source
