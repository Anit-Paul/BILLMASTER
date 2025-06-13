from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import product
from login.views import user,home_operation
from login.models import account
from .pdf import pdf
from django.core.mail import EmailMessage
from login.models import account

class operations:
    def add_product(self,request):
        return render(request, 'bill/index.html')

    def view_product(self,request):
        if request.method == 'POST':
            search = request.POST.get('search', '').strip()
            user_email = user().get_user(request)

            if search and user_email:
                search_upper = search.upper()
                products_by_name = product.objects.filter(user_id=user_email, product_name__icontains=search_upper)
                products_by_description = product.objects.filter(user_id=user_email, description__icontains=search_upper)
                products = list(products_by_name) + list(products_by_description)
                return render(request, 'bill/view_product.html', {'products': products})

        user_email = user().get_user(request)
        products = list(product.objects.filter(user_id=user_email))
        return render(request, 'bill/view_product.html', {'products': products})

    @staticmethod
    def get_bill(request):
        return render(request, 'bill/get_bill.html')
    
    @staticmethod
    def is_present(name, desc):
        return list(product.objects.filter(product_name=name.upper(), description=desc.upper()))

    def save(self,request):
        try:
            name = request.POST.get('pname', '').strip()
            user_email = user().get_user(request)  # Retrieve email from session

            if not user_email:
                return redirect('get_login')  # Redirect to login if no user email found in session

            quantity = request.POST.get('quantity', '').strip()
            cost = request.POST.get('cost', '').strip()
            desc = request.POST.get('desc', '').strip()

            if not name:
                return render(request, 'bill/index2.html', {'msg': 'Please enter a product name!'})
            if not quantity.isdigit() or int(quantity) <= 0:
                return render(request, 'bill/index2.html', {'msg': 'Quantity must be a positive number!'})
            if not cost.isdigit() or int(cost) <= 0:
                return render(request, 'bill/index2.html', {'msg': 'Cost must be a positive number!'})

            try:
                user_data = account.objects.get(email=user_email)
            except account.DoesNotExist:
                return redirect('get_login')

            existing_products = self.is_present(name, desc)
            if existing_products:
                for product_instance in existing_products:
                    product_instance.product_quantity += int(quantity)
                    product_instance.cost = int(cost)
                    product_instance.save()
            else:
                new_product = product(product_name=name.upper(), user=user_data, description=desc.upper(),
                                    product_quantity=int(quantity), cost=int(cost))
                new_product.save()

            return render(request, 'home/index.html')

        except Exception as e:
            return render(request, 'bill/index2.html', {'msg': f'An error occurred: {str(e)}'})

    def bill_page(self,request):
        items_list = request.session.get('items_list', [])
        cost=0
        for i in items_list:
            cost+=i['cost']
        return render(request, 'bill/bill.html', {'products': items_list,'cost':cost,'email':user().get_user(request)})

    def update_list(self,request, product_instance,q):
        item = {
            'product_name': product_instance.product_name,
            'quantity':q,
            'description': product_instance.description,
            'cost': product_instance.cost*q,
        }
        items = request.session.get('items_list', [])
        items.append(item)
        request.session['items_list'] = items

    def add_bill(self,request):
        product_name = request.POST.get('pname', '').strip()
        quantity = request.POST.get('quantity', '').strip()
        description = request.POST.get('desc', '').strip()

        if not product_name or not quantity.isdigit() or int(quantity) <= 0:
            return render(request, 'bill/get_bill2.html', {'msg': 'Invalid input. Please provide valid details.'})

        user_email = user().get_user(request)
        try:
            # Correctly retrieve a single product instance or raise an exception
            product_instance = product.objects.get(user_id=user_email, product_name=product_name.upper(),
                                                description=description.upper())

            if product_instance.product_quantity < int(quantity):
                return render(request, 'bill/get_bill2.html', {'msg': 'Insufficient Items!'})

            # Update the product quantity
            product_instance.product_quantity -= int(quantity)
            product_instance.save()

            # Optional: Update session list
            self.update_list(request, product_instance,int(quantity))

            return render(request, 'bill/get_bill3.html', {'msg': 'Item added successfully!'})

        except product.DoesNotExist:
            return render(request, 'bill/get_bill2.html', {'msg': 'Product not found.'})
        except Exception as e:
            return render(request, 'bill/get_bill2.html', {'msg': f'An error occurred: {str(e)}'})
        
    def generate(self,request):
        return render(request,'bill/bill_option.html')
        
    @staticmethod
    def delete_product(request):
        return render(request,'bill/delete.html')
    
    @staticmethod
    def delete(request):
        name=request.POST.get('pname','').strip()
        desc=request.POST.get('desc','').strip()
        a=product.objects.filter(user_id=user().get_user(request),product_name=name.upper(),description=desc.upper())
        a.delete()
        return render(request,'home/index.html')

    def get_copy(self,request):
        items_list = request.session.get('items_list', [])
        cost = sum(item['cost'] for item in items_list)  # Calculate the total cost
        email=user().get_user(request)
        context = {
            'products': items_list,
            'cost': cost,
            'email':email
        }
        a=pdf()
        p = a.html2pdf('bill/bill.html', context)  # Pass context to the PDF generation function

        if p:  
            request.session['items_list'] = []
            return p
        else:
            return HttpResponse("Error generating PDF", content_type="text/plain")
        
    def send_mail(self, request):
        return render(request,'bill/customer_details.html')
    def sended(self,request,mail):
        # Email subject
        a=account.objects.filter(email=user().get_user(request))
        
        message_name = f'Invoice from {a[0].name}'
        
        # Retrieve items and calculate the total cost
        items_list = request.session.get('items_list', [])
        cost = sum(item['cost'] for item in items_list)
        
        # Get the user's email
        email = user().get_user(request)
        
        # Prepare context for PDF generation
        context = {
            'products': items_list,
            'cost': cost,
            'email': email
        }
        
        # Generate PDF
        a = pdf()
        p = a.html2pdf('bill/bill.html', context)
        
        # Create an email message
        email_message = EmailMessage(
            subject=message_name,
            body="Please find attached your Bill.",
            from_email=email,
            to=[mail],
        )
        
        # Attach the PDF to the email
        if isinstance(p, HttpResponse):
            email_message.attach('Bill.pdf', p.content, 'application/pdf') 
        else:
            email_message.attach('invoice.pdf', p, 'application/pdf')
        
        # Send the email
        email_message.send()
        request.session['items_list'] = []
        return render(request,'home/index.html')
    
    def pre_send(self,request):
        obj=home_operation()
        a = request.POST.get('cemail')
        b = request.POST.get('cemail2')
        if not obj.valid(a) or not obj.valid(b):
            map={
                'msg':'Enter a Valid Email!'
            }
            return render(request,'bill/customer_details.html',map)
        if a!=b:
            map={
                'msg':'Enter same emails Email!'
            }
            return render(request,'bill/customer_details.html',map)
        self.sended(request,a)
        return render(request, 'home/index.html', {'msg': 'Email sent successfully!'})