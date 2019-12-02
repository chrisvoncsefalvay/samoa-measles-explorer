import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Mortality/Morbidity", href="/mortality-morbidity")),
        dbc.NavItem(dbc.NavLink("By age group", href="/by-age-group")),
        dbc.NavItem(dbc.NavLink("CFR", href="/cfr"))
        # dbc.NavItem(dbc.NavLink("About", href="/about")),
    ],
    brand="Samoa Measles Crisis 🇼🇸",
    brand_href="/",
    sticky="top",
)
