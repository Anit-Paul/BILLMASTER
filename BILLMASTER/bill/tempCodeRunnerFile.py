try:
            user = account.objects.get(email=user_email)
        except account.DoesNotExist:
            return redirect('get_login')  # Redirect to login if the user is not found

        lst = is_present(name, desc)
        if len(lst) != 0:
            for i in range(len(lst)):
                lst[i].product_quantity += int(quantity)
                lst[i].cost = cost
                lst[i].save()
        else:
            p = product(product_name=name.upper(), user=user, description=desc.upper(), product_quantity=int(quantity), cost=int(cost))
            p.save()
