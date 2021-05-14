from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from decouple import config


API_KEY = str(config('API_KEY'))

# Create your views here.

def home(request):
    # to return results to html page
    context = {}

    import requests
    import json


    if request.method == 'POST':
        ticker = str(request.POST['ticker'])
        length_of_ticker = len(ticker.split(','))

        # create an account on rapidapi to use 
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"

        # visit this site to look for ticker symbol - https://www.marketwatch.com/tools/quotes/lookup.asp

        # e.g ticker = 'amzn,aapl,goog,fb'
        querystring = {"region":"IN","symbols":ticker}

        headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
            }

        # call to the api
        response = requests.request("GET", url, headers=headers, params=querystring)

        try:
            res = json.loads(response.content)
            print('length = ', len(res['quoteResponse']['result']))
            if len(res['quoteResponse']['result']) > 0 :
                # print('i am here\n')
                # list to store key value pair company wise
                tickers = []
                # retriving important results from the api call response
                for i in range(0,length_of_ticker):
                    temp = {}
                    # temp['company'] = res['quoteResponse']['result'][i]['longName']
                    temp['company'] = res['quoteResponse']['result'][i].get('longName')
                    temp['quoteType'] = res['quoteResponse']['result'][i].get('quoteType')
                    temp['currency'] = res['quoteResponse']['result'][i].get('currency')
                    temp['stockPrice'] = res['quoteResponse']['result'][i].get('regularMarketPrice')
                    temp['previousClose'] = res['quoteResponse']['result'][i].get('regularMarketPreviousClose')
                    temp['bidSize'] = res['quoteResponse']['result'][i].get('bidSize')
                    temp['askSize'] = res['quoteResponse']['result'][i].get('askSize')
                    temp['trailingPE'] = res['quoteResponse']['result'][i].get('trailingPE')
                    temp['forwardPE'] = res['quoteResponse']['result'][i].get('forwardPE')
                    temp['marketCap'] = res['quoteResponse']['result'][i].get('marketCap')
                    temp['fiftyTwoWeekLow'] = res['quoteResponse']['result'][i].get('fiftyTwoWeekLow')
                    temp['fiftyTwoWeekHigh'] = res['quoteResponse']['result'][i].get('fiftyTwoWeekHigh')
                    temp['fiftyTwoWeekRange'] = res['quoteResponse']['result'][i].get('fiftyTwoWeekRange')
                    tickers.append(temp)

                # to check output in console
                # for elements in tickers:
                    # for key, val in elements.items():
                        # print(key,'->', val)
                    # print()

                context['tickers'] = tickers

            else:
                print('i an in the error\n')
                context['tickers'] = 'error...'

        except Exception as e:
            print('exception----->',e)
            context['tickers'] = 'error...'

        return render(request, 'home.html', context)

    else:
        return render(request, 'home.html', {'empty':'Enter company\'s ticker symbol in the search box and hit search......'})

def about(request):
    context = {}
    return render(request, 'about.html', context)

def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, 'Stock Has Been Added Successfully')
            return redirect('add_stock')

    else:
        import requests
        import json
        tickers = Stock.objects.all()
        context = {}


        symbols = ''
        ids = []
        for item in tickers:
            # print('item id = ',item.id)
            ids.append(item)
            symbols += str(item)+','
        symbols = symbols[:-1]
        # context['ids'] = ids
        output = []


        # create an account on rapidapi to use 
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"

        # visit this site to look for ticker symbol - https://www.marketwatch.com/tools/quotes/lookup.asp

        # e.g ticker = 'amzn,aapl,goog,fb'
        querystring = {"region":"IN","symbols":symbols}

        headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
            }

        # call to the api
        response = requests.request("GET", url, headers=headers, params=querystring)

        err = ''

        try:
            length_of_ticker = len(symbols.split(','))
            # print(length_of_ticker)

            res = json.loads(response.content)
            # print('len of request = ', length_of_ticker, '------len of response = ', len(res['quoteResponse']['result']))
            if length_of_ticker > len(res['quoteResponse']['result']):
                messages.success(request, 'Invalid input deleting this stock')
                return delete(request, ids[len(ids)-1].id)
            else:
                # print('length = ', len(res['quoteResponse']['result']))
                if len(res['quoteResponse']['result']) > 0 :
                    # print('i am here\n')
                    # list to store key value pair company wise
                    # tickers = []
                    # retriving important results from the api call response
                    for i in range(0,length_of_ticker):
                        temp = {}
                        temp['symbol'] = res['quoteResponse']['result'][i].get('symbol')
                        temp['company'] = res['quoteResponse']['result'][i].get('longName')
                        temp['quoteType'] = res['quoteResponse']['result'][i].get('quoteType')
                        temp['currency'] = res['quoteResponse']['result'][i].get('currency')
                        temp['stockPrice'] = res['quoteResponse']['result'][i].get('regularMarketPrice')
                        temp['previousClose'] = res['quoteResponse']['result'][i].get('regularMarketPreviousClose')
                        temp['bidSize'] = res['quoteResponse']['result'][i].get('bidSize')
                        temp['askSize'] = res['quoteResponse']['result'][i].get('askSize')
                        temp['trailingPE'] = res['quoteResponse']['result'][i].get('trailingPE')
                        temp['forwardPE'] = res['quoteResponse']['result'][i].get('forwardPE')
                        temp['marketCap'] = res['quoteResponse']['result'][i].get('marketCap')
                        temp['fiftyTwoWeekLow'] = res['quoteResponse']['result'][i].get('fiftyTwoWeekLow')
                        temp['fiftyTwoWeekHigh'] = res['quoteResponse']['result'][i].get('fiftyTwoWeekHigh')
                        temp['fiftyTwoWeekRange'] = res['quoteResponse']['result'][i].get('fiftyTwoWeekRange')
                        temp['floatShares'] = res['quoteResponse']['result'][i].get('floatShares')
                        temp['marketVolume'] = res['quoteResponse']['result'][i].get('regularMarketVolume')
                        temp['priceToSales'] = res['quoteResponse']['result'][i].get('priceToSales')
                        temp['revenue'] = res['quoteResponse']['result'][i].get('revenue')
                        temp['pegRation'] = res['quoteResponse']['result'][i].get('pegRation')
                        output.append(temp)

                    # to check output in console
                    # for elements in output:
                        # for key, val in elements.items():
                            # print(key,'->', val)
                        # print()

                    # context['tickers'] = tickers

                else:
                    print('in the error\n')
                    # context['tickers'] = 'error...'
                    # output.append({'error':'error...'})
                    err = 'error...'

        except Exception as e:
            print('exception--->',e)
            # context['tickers'] = 'error...'
            # output.append({'error':'error...'})
            err = 'error...'
        

        zipped_data = zip(ids,output)
        return render(request, 'add_stock.html', {'zipped_data':zipped_data, 'tickers':tickers, 'output':output, 'err':err})

def delete(request, stock_id=None):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, 'Stock Has Been Deleted Successfully')
    # changed here
    return redirect('add_stock')
    # return render(request, 'add_stock.html', {})
