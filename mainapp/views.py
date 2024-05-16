from stocksapp.models import Stock
from stocksapp.stocks import StockScraper
from django.contrib import messages
from django.views.generic import ListView #, DetailView, CreateView, UpdateView, TemplateView, DeleteView



###################################################
#                    Home                         #
###################################################

class HomeView(ListView):
    model = Stock
    paginate_by = 10
    template_name = 'mainapp/home.html'

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

print(100*'8B',' ==>', Stock)
