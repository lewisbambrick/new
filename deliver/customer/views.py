from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Catagory, OrderModel

class Index(View):
    def get(self, request, *args, **kwargs):
        return render (request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render (request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        
        #get every item from each catagory
        appetizers = MenuItem.objects.filter(catagory__name__contains='Appetizer')
        entres = MenuItem.objects.filter(catagory__name__contains='Entre')
        desserts = MenuItem.objects.filter(catagory__name__contains='Dessert')
        drinks = MenuItem.objects.filter(catagory__name__contains='Drink')
        #pass into context
        context= {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks
        }
        #render the template

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):

        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        county = request.POST.get('county')
        post_code = request.POST.get('postcode')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
            
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            county=county,
            post_code=post_code
            )
        order.items.add(*item_ids)

        #after everything is done send confirmation email to user
        body = ('Thank you for your order! Your food is being made and will be delivered soon.\n'
                f'Your Total: {price}\n'
                'Thank you again for your order')

        send_mail(
            'Thank you for your Order!',
            body,
            'example@email.ie',
            [email],
            fail_silently=False
        )

        context = {

            'items': order_items['items'],
            'price': price
        }
        return redirect('order-confirmation', pk=order.pk)
       
            

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,


        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        print(request.body)
        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')