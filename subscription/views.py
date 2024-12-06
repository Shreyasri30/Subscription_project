from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Product, Subscription
from datetime import datetime, date
from django.shortcuts import render
import json
import uuid
from django.db.models import Q

@csrf_exempt
def customer_list(request):
    if request.method == "GET":
        customers = Customer.objects.all().values('customer_id', 'name')
        return JsonResponse(list(customers), safe=False, status=200)

@csrf_exempt
def add_customer(request):
    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        name = request.POST.get('name')

        if Customer.objects.filter(customer_id=customer_id).exists():
            return JsonResponse({'error': 'Customer already exists'}, status=400)
        customer = Customer.objects.create(customer_id=customer_id, name=name)
        return JsonResponse({'message': 'Customer added successfully'}, status=201)
    return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)

@csrf_exempt
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all().values('id', 'product_name')
        return JsonResponse(list(products), safe=False, status=200)


@csrf_exempt
def add_subscription(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            required_fields = ['customer_id', 'product_id', 'start_date', 'end_date']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'{field.replace("_", " ").title()} is required'}, status=400)
            
            subscription = Subscription.objects.create(
                customer=Customer.objects.get(customer_id=data['customer_id']),
                product=Product.objects.get(id=data['product_id']),
                start_date=data['start_date'],
                end_date=data['end_date'],
                users=data.get('users', 1)
            )
            
            return JsonResponse({
                'message': 'Subscription added successfully', 
                'subscription_id': str(subscription.subscription_id)
            }, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Error processing subscription: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def extend_subscription(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subscription_id = data.get('subscription_id')

            if not subscription_id:
                return JsonResponse({'error': 'Subscription ID is required'}, status=400)

            try:
                subscription_uuid = uuid.UUID(str(subscription_id))
                subscription = Subscription.objects.get(
                    Q(subscription_id=subscription_uuid) | Q(id=subscription_uuid)
                )
                
                new_end_date_str = data.get('new_end_date')
                if not new_end_date_str:
                    return JsonResponse({'error': 'New end date is required'}, status=400)

                new_end_date = datetime.strptime(new_end_date_str, '%Y-%m-%d').date()
                
                subscription.end_date = new_end_date
                subscription.save()
                return JsonResponse({
                    'message': 'Subscription extended successfully',
                    'new_end_date': new_end_date.isoformat()
                }, status=200)

            except ValueError:
                return JsonResponse({'error': 'Invalid Subscription ID format'}, status=400)
            except Subscription.DoesNotExist:
                return JsonResponse({'error': 'Subscription not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"Error extending subscription: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)

@csrf_exempt
def end_subscription(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subscription_id = data.get('subscription_id')

            if not subscription_id:
                return JsonResponse({'error': 'Subscription ID is required'}, status=400)

            try:
                subscription_uuid = uuid.UUID(str(subscription_id))
                subscription = Subscription.objects.get(
                    Q(subscription_id=subscription_uuid) | Q(id=subscription_uuid)
                )

                subscription.end_date = date.today()
                subscription.save()
                return JsonResponse({'message': 'Subscription ended successfully'}, status=200)

            except ValueError:
                return JsonResponse({'error': 'Invalid Subscription ID format'}, status=400)
            except Subscription.DoesNotExist:
                return JsonResponse({'error': 'Subscription not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"Error ending subscription: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)

@csrf_exempt
def revenue_report(request):
    if request.method == "GET":
        try:
            subscriptions = Subscription.objects.select_related('product').all()
            total_revenue = sum(
                sub.users * (sub.product.annual_cost or 0) 
                for sub in subscriptions 
                if sub.product
            )
            return JsonResponse({'total_revenue': total_revenue}, status=200)
        except Exception as e:
            print(f"Error generating revenue report: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)