# from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView #, DetailView, View, CreateView, UpdateView, TemplateView, DeleteView
from django.contrib import messages
#from django.http import Http404
from .stocks import StockScraper
from .models import Stock
#from .forms import StockForm



class HomeView(ListView):
    model = Stock
    paginate_by = 10
    template_name = 'stocksapp/home.html'
    context_object_name = 'stock'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            stocks = Stock.objects.all()
            print('Stocks ==>', stocks)
            stock_data = []
            for stock in stocks:
                print(50*'<==>', type(stock.symbol))
                scraper = StockScraper(stock.symbol)
                data = scraper.scrape_stock_data()
                stock_data.append(data)
            context['stock_data'] = stock_data
            print(50*'#','Stocks ==>', stock_data)
        except:
            messages.info(self.request, 'Sorry Couldnt get anything...')
        return context

