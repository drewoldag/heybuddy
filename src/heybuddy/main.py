from flask import Flask, render_template
from bokeh.embed import components
from bokeh.models import Span, Whisker
from bokeh.plotting import figure
from bokeh.resources import INLINE

app = Flask(__name__)

@app.route('/hello/<name>')
def hello_world(name):
    return "Hello %s" % name

@app.route('/bokeh')
def bokeh():
    fig = figure(sizing_mode="stretch_width", height=600)
    fig.step(
        x=[1,2,3,4],
        y=[1.7, 2.2, 4.6, 3.9],
        mode='after',
        color='navy',
        legend_label='Metric 1',
        line_width=2,
    )

    error_test = Whisker(base=2, upper=2.4, lower=2.0,
                level="annotation", line_width=1, dimension="height", line_color='navy')

    fig.add_layout(error_test)

    fig.step(
        x=[1,2,3,4,5],
        y=[1.0, 0.8, 0.65, 0.5, 0.45],
        mode='after',
        color='red',
        legend_label='Metric 2',
        line_width=2
    )

    error_test = Whisker(base=3, upper=0.7, lower=0.6,
                level="annotation", line_width=1, dimension="height", line_color='red')
    
    fig.add_layout(error_test)

    test_span = Span(location=2.5, dimension='height', line_color='blue', line_width=1, line_dash='dashed', line_join='round')

    fig.add_layout(test_span)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)

    return render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources
    )

if __name__ == '__main__':
    app.run()