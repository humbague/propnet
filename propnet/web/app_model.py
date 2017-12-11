import dash_html_components as html
import dash_core_components as dcc

from propnet.properties import get_display_name
from propnet.web.utils import references_to_markdown

import propnet.models as models

# layouts for model detail pages

def model_image_component(model):

    url = "https://robohash.org/{}".format(model.__hash__())
    return html.Img(src=url, style={'width': 150, 'border-radius':'50%'})

def model_layout(model_name):
    """
    Create a Dash layout for a provided model.

    :param model: an instance of an AbstractModel subclass
    :return: Dash layout
    """

    # instantiate model from name
    # TODO: horrendous hack, fix propnet.models.__init__
    model = getattr(getattr(models, model_name), model_name)()

    if model.tags:
        tags = html.Ul(className="tags", children=[
                html.Li(tag, className="tag") for tag in model.tags
        ])
    else:
        tags = None

    badge = html.Div(className='double-val-label', children=[
        html.Span('model-id', className='model'),
        html.Span('{}-rev{}'.format(model.__hash__(), model.revision))
    ])


    title = html.Div(className='row', children=[
        html.Div(className='three columns', style={'text-align': 'right'}, children=[
            model_image_component(model)
        ]),
        html.Div(className='nine columns', children=[
            html.H3(model.title),
            badge
        ])
    ])

    if model.references:
        references = dcc.Markdown(references_to_markdown(model.references))
    else:
        # TODO: append to list instead ...
        references = None

    symbols_layout = html.Div(children=[
        html.Div(className='row', children=[
            html.Div(className='two columns', children=[str(symbol)]),
            html.Div(className='ten columns', children=[dcc.Link(get_display_name(property_name),
                                                                 href='/property/{}'.format(property_name))])
        ])
        for symbol, property_name in model.symbol_mapping.items()
    ])

    # TODO: change equations to property
    equations_layout = html.Div(children=[
        html.Div(className='row', children=[equation])
        for equation in model.equations
    ])

    #method = model.method TODO: add below description

    # TODO
    breadcrumb = html.Div()

    return html.Div([
        breadcrumb,
        title,
        html.Br(),
        html.H6('References'),
        references,
        html.H6('Symbols'),
        symbols_layout,
        html.H6('Equations'),
        equations_layout,
        html.H6('What this model does'),
        dcc.Markdown(model.description),
        # dcc.Markdown("Method: {}".format(model.method)),
        html.H6('Tags'),
        tags
    ])

model_links = html.Div([
    html.Div([
        dcc.Link(model_name, href='/model/{}'.format(model_name)),
        html.Br()
    ])
    for model_name in models.all_model_names
])

models_index = html.Div([
    html.H5('Current models:'),
    model_links,
    html.Br(),
    dcc.Link('< Back', href='/')
])