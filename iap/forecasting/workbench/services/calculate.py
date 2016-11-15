

def load_formulas(self, instructions):
    # Calculation engine
    init_calc_engine(self.kernel, instructions)


def calculate(calc_engine, container):
    calc_engine.calculate(container, container.timeline, 'main', period_ali='all')
    calc_engine.calculate(container, container.timeline, 'country_growth', in_period=('2013', '2014'))
    calc_engine.calculate(container, container.timeline, 'category_growth', in_period=('2013', '2014'))
    calc_engine.calculate(container, container.timeline, 'country_growth', in_period=('2014', '2015'))
    calc_engine.calculate(container, container.timeline, 'category_growth', in_period=('2014', '2015'))
    calc_engine.calculate(container, container.timeline, 'country_growth', in_period=('2015', '2016'))
    calc_engine.calculate(container, container.timeline, 'category_growth', in_period=('2015', '2016'))
    calc_engine.calculate(container, container.timeline, 'country_growth', in_period=('2016', '2017'))
    calc_engine.calculate(container, container.timeline, 'category_growth', in_period=('2016', '2017'))
    calc_engine.calculate(container, container.timeline, 'country_growth', in_period=('2017', '2018'))
    calc_engine.calculate(container, container.timeline, 'category_growth', in_period=('2017', '2018'))
    #calc_engine.calculate(container, container.timeline, 'decomposition', in_period=('2013', '2014'))
    #calc_engine.calculate(container, container.timeline, 'decomposition', in_period=('2014', '2015'))
    #calc_engine.calculate(container, container.timeline, 'decomposition', in_period=('2015', '2016'))
    #calc_engine.calculate(container, container.timeline, 'decomposition', in_period=('2016', '2017'))
    #calc_engine.calculate(container, container.timeline, 'decomposition', in_period=('2017', '2018'))
    #calc_engine.calculate(container, container.timeline, 'decomposition', in_period=('2013', '2015'))
    #calc_engine.calculate(container, container.timeline, 'decomposition', in_period=('2015', '2018'))
    return