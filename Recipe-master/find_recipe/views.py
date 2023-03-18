from django.shortcuts import render
from django.views import generic
from dashboard.models import Recipe,Categories,RecipeTips
from django.http import HttpRequest, JsonResponse
from django.db.models import Q
# Create your views here.



class FindRecipeView(generic.ListView):
    template_name = "find-recipe.html"  
    context_object_name  = 'recipes'
   
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['q']=self.request.GET.get('q')
        context['category_list']=Categories.objects.filter(id__in=self.request.GET.getlist('id'))
        context['category'] = Categories.objects.all()
        context['tips'] = RecipeTips.objects.all().order_by('-id')
        return context
    
    def get_queryset(self):
        query=Recipe.objects.filter(status=True)
        
        if self.request.GET.getlist('id'):
            query=query.filter(category__in = Categories.objects.filter(id__in=self.request.GET.getlist('id')))
        if self.request.GET.get('q'):
            q=self.request.GET.get('q')

            query=query.filter(
                 Q(name__icontains=self.request.GET.get('q')) | 
                 Q(description__icontains=self.request.GET.get('q')) |
                 Q(category__name__icontains = self.request.GET.get('q')))
            
            if query:
                pass
            else:
               
                query=Recipe.objects.filter(status=True)
                for data in q.split(' '):
                    query=Recipe.objects.filter(status=True).filter(name__icontains = data)
                   
                    if self.request.GET.getlist('id'):
                        query=query.filter(category__in = Categories.objects.filter(id__in=self.request.GET.getlist('id')))
  
        return query
class RecipeDetailView(generic.DetailView):
    template_name = "detail.html"
    context_object_name= 'instance' 
    queryset=Recipe.objects.all()

class RatingRecipeView(generic.View):   
    def post(self,request):
        value=request.POST.get('value')
        id=request.POST.get('id')     
        ins = Recipe.objects.get(id=id)
        
        print(value,id)
        
        if ins.no_of_user_rated_points_1 or value == '1':
            if value == '1' :
                if ins.no_of_user_rated_points_1:
                    ins.no_of_user_rated_points_1 = ins.no_of_user_rated_points_1+1
                    one= ins.no_of_user_rated_points_1
                else:
                    ins.no_of_user_rated_points_1 = 1 
                    one = 1
            else:
                one =  ins.no_of_user_rated_points_1
        else:
            ins.no_of_user_rated_points_1 = 0
            one=0
        
        if ins.no_of_user_rated_points_2 or value == '2':
            if value == '2' :
                if ins.no_of_user_rated_points_2:
                    ins.no_of_user_rated_points_2 = ins.no_of_user_rated_points_2+1
                    two = ins.no_of_user_rated_points_2
                else:
                    ins.no_of_user_rated_points_2 = 1
                    two = 1
            else:
                two =  ins.no_of_user_rated_points_2
        else:
            ins.no_of_user_rated_points_2 = 0
            two = 0
        
        if ins.no_of_user_rated_points_3 or value == '3':
            if value == '3' :
                if  ins.no_of_user_rated_points_3:
                    ins.no_of_user_rated_points_3 = ins.no_of_user_rated_points_3 + 1
                    three =ins.no_of_user_rated_points_3
                else:
                    ins.no_of_user_rated_points_3 = 1
                    three = 1
            else:
                three = ins.no_of_user_rated_points_3
        else:
            ins.no_of_user_rated_points_3 = 0
            three = 0
        
        if ins.no_of_user_rated_points_4 or value == '4':
            if value == '4' :
                if ins.no_of_user_rated_points_4:
                    ins.no_of_user_rated_points_4 = ins.no_of_user_rated_points_4 + 1
                    four= ins.no_of_user_rated_points_4
                else:
                    ins.no_of_user_rated_points_4 = 1
                    four =1
            else:
                four= ins.no_of_user_rated_points_4
        else:
            ins.no_of_user_rated_points_4 = 0
            four =0
        
        if ins.no_of_user_rated_points_5 or value == '5':
            if value == '5' :
                if ins.no_of_user_rated_points_5:
                    ins.no_of_user_rated_points_5 = ins.no_of_user_rated_points_5 + 1
                    five= ins.no_of_user_rated_points_5
                else:
                    ins.no_of_user_rated_points_5 = 1
                    five = 1
            else:
                five= ins.no_of_user_rated_points_5
        else:
            ins.no_of_user_rated_points_5= 0 
            five = 0
        ins.save()
        
        sum_of_rating= one*1 +  two *2 + three*3 + four*4 + five*5
        total_rating= one + two + three + four + five
        avg=sum_of_rating/total_rating
        ins.rating_points_avg = avg
        ins.save()
        return JsonResponse({'status':1})
    

    
    

     
    