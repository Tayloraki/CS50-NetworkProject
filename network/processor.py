def add_user(request):
   context = {
       'user': request.user
   }
   return context