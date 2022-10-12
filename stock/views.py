#Created by Idrees Khan/ Travis Taylor

from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import tickersymbol
from .forms import searchform
import yfinance as yf
import plotly.graph_objects as go
import plotly.offline as opy
import plotly.express as px
posts = [
    {
        'author': 'First Pick: ',
        'title': 'Motley Fool',
        'number': '#1',
        'content': 'Motley Fool is an investment site for new to experienced investors. The site provides a variety of services from top stock picks to investment basics such as type of stocks and investment advice for each type.',
        'price': 'https://www.fool.com/',
    },
    {
        'author': 'Second Pick: ',
        'title': 'Seeking Alpha',
        'number': '#2',
        'content': 'Seeking Alpha can seem intimidating at first but it has all the essential information to get started on the first page. The site provides top stocks, latest news, and an educational page with articles and videos for the user.',
        'price': 'https://seekingalpha.com/',
    },
    {
        'author': 'Third Pick: ',
        'title': 'Stock Rover',
        'number': '#3',
        'content': 'Stock Rover is a website aimed at providing the best investment research for investors. They provide their best buy and hold options along with screening strategies and portfolio management.',
        'price': 'https://www.stockrover.com/',
    },
    {
        'author': 'Fourth Pick: ',
        'title': 'Investopedia',
        'number': '#4',
        'content': 'This website provides some of the best educational tools for new investors on the market. It highlights key terms and vital investment strategies. It also provides investment simulators to try and learn those strategies.',
        'price': 'https://www.investopedia.com/',
    },
    {
        'author': 'Fifth Pick: ',
        'title': "Barron's",
        'number': '#5',
        'content': 'Barron is a little different from the other sources. It provides weekly stock recommendations and daily market insights. They provides 5 different stock options based on different strategies.',
        'price': 'https://www.fool.com/',
    },
]

# Create your views here.
class TickerSearch(CreateView):
    model = tickersymbol
    template_name = 'stock/home.html'
    form_class = searchform


def learn(request):
    context = {
        'posts': posts
    }
    return render(request, 'stock/learn.html', context)

def portfolio(request):
    stock = tickersymbol.objects.last()
    yahoo_stock = yf.Ticker(stock.ticker)
    revenue = yahoo_stock.quarterly_earnings['Revenue']
    earnings = yahoo_stock.quarterly_earnings['Earnings']
    distribution = yahoo_stock.major_holders
    df =  yahoo_stock.history(period="1mo")
    old = df.reset_index()
    for i in ['Open', 'High', 'Close', 'Low']: 
        old[i]  =  old[i].astype('float64')

    fig = go.Figure(data=[go.Candlestick(x=old['Date'],open=old['Open'],high=old['High'],low=old['Low'],close=old['Close'])])
    graph = opy.plot(fig, auto_open=False, output_type='div')
    linefig = px.line(old, x="Date", y="Open", title='Stock Prices')
    linegraph = opy.plot(linefig, auto_open=False, output_type='div')
    content = { 'ask' : yahoo_stock.info['ask'],
                'bid' : yahoo_stock.info['bid'],
                'spread' : round(yahoo_stock.info['ask'] - yahoo_stock.info['bid'],2),
                'name' : yahoo_stock.info['shortName'],
                'sector' : yahoo_stock.info['sector'],
                'employees' : yahoo_stock.info['fullTimeEmployees'],
                'description' : yahoo_stock.info['longBusinessSummary'],
                'pegratio' : yahoo_stock.info['pegRatio'],
                'open' : yahoo_stock.info['open'],
                's1' : distribution[0][0],
                's2' : distribution[0][1],
                's3' : distribution[0][2],
                's4' : distribution[0][3],
                's5' : distribution[1][0],
                's6' : distribution[1][1],
                's7' : distribution[1][2],
                's8' : distribution[1][3],
                'graph' : graph,
                'linegraph' : linegraph,
                'revenue' : '{:20,}'.format(revenue[0] + revenue[1] + revenue[2] + revenue[3]),
                'earnings' : '{:20,}'.format(earnings[0] + earnings[1] + earnings[2] + earnings[3])}
    return render(request, 'stock/portfolio.html', content)




















