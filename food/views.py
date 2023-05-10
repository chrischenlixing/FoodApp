from django.shortcuts import redirect, render
from django.http import HttpResponse

from food.forms import ItemForm
from .models import Item
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    item_list = Item.objects.all()
    context = {
        'item_list' : item_list,
    }
    paginator = Paginator(item_list,2)
    page = request.GET.get('page')
    food_objects = paginator.get_page(page)
    return render(request,'food/index.html',context)

class IndexClassView(ListView):
    model = Item
    template_name = 'food/index.html'
    context_object_name ='item_list'
    paginate_by = 3



class CreateItem(CreateView):
    model = Item
    fields = ['item_name','item_desc','item_price','item_image']
    template_name = 'food/item-form.html'

    def form_valid(self,form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

def item(request):
    return HttpResponse('<h1>This is an item view<h1>')

def detail(request,item_id):
    item = Item.objects.get(pk = item_id)
    context = {
        'item' : item
    }
    return render(request,'food/detail.html',context)

class FoodDetail(DetailView):
    model = Item
    template_name = 'food/detail.html' 

def create_item(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('food:index')
    return render(request,'food/item-form.html',{'form':form})

def update_item(request,id):
    item =Item.objects.get(id = id)
    form = ItemForm(request.POST or None, instance = item)

    if form.is_valid():
        form.save()
        return redirect('food:index')
    
    return render(request,'food/item-form.html',{'form':form,'item':item})

def delete_item(request,id):
    item = Item.objects.get(id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('food:index')
    
    return render(request,'food/item-delete.html',{'item':item})