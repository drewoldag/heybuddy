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
    fig = figure(sizing_mode="stretch_width", height=600, x_axis_type="datetime")

    fig.step(
        x=[1,2,3,4],
        y=[1, 2.2, 4.6, 3.9],
        mode='after',
        color='navy',
        legend_label='Metric 1',
        line_width=2,
    )
    fig.circle(x=[1,2,3,4],
        y=[1, 2.2, 4.6, 3.9], legend_label='Metric 1', color='navy')

    error_test = new_whisker(base=2, upper=2.4, lower=2.0)
    fig.add_layout(error_test)

    fig.step(
        x=[1,2,3,4,5],
        y=[1.0, 0.8, 0.65, 0.5, 0.45],
        mode='after',
        color='red',
        legend_label='Metric 2',
        line_width=2
    )

    fig.circle(x=[1,2,3,4,5],
        y=[1.0, 0.8, 0.65, 0.5, 0.4], color='red', legend_label='Metric 2')

    error_test = new_whisker(base=3, upper=0.7, lower=0.6)
    fig.add_layout(error_test)

    test_span = Span(location=2.5, dimension='height', line_color='blue', line_width=1, line_dash='dashed')
    fig.add_layout(test_span)

    fig.legend.click_policy = "mute"

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

def new_whisker(base, upper, lower):
    w = Whisker(base=base, upper=upper, lower=lower,
                level="annotation", line_width=1, dimension="height", line_color='black')
    w.upper_head.size=4
    w.lower_head.size=4

    return w

if __name__ == '__main__':
    app.run(host='0.0.0.0')