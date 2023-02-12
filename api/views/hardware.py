from datetime import datetime

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count, Q

from hardware.models import (
    Laptop,
    LaptopBrand,
    Building
)
from api.serializers import (
    LaptopSerializer,
    LaptopBrandSerializer,
    BuildingSerializer
)

class LaptopViewSet(viewsets.ModelViewSet):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer

class LaptopBrandViewSet(viewsets.ModelViewSet):
    queryset = LaptopBrand.objects.all()
    serializer_class = LaptopBrandSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

# Chart APIs
class LaptopChartAPI(APIView):
    def get(self, request):
        response = {
            "laptop_status": {
                "labels": [],
                "datasets": [{
                    "label": "# of Laptops",
                    "data": []
                }]
            },
            "laptop_branch": {
                "labels": [],
                "datasets": [{
                    "label": "# of Laptops",
                    "data": []
                }]
            },
            "laptop_availability": {
                "labels": [],
                "datasets": [{
                    "label": "# of Laptops",
                    "data": []
                }]
            },
            "laptop_age": {
                "labels": [],
                "datasets": [{
                    "label": "# of Laptops",
                    "data": []
                }]
            }
        }
        laptop_status_data = Laptop.objects.values('laptop_status').annotate(total=Count('id'))
        for data in laptop_status_data:
            response['laptop_status']['labels'].append(data['laptop_status'])
            response['laptop_status']['datasets'][0]['data'].append(data['total'])
        
        laptop_branch_data = Laptop.objects.values('laptop_branch__location').annotate(total=Count('id'))
        for data in laptop_branch_data:
            response['laptop_branch']['labels'].append(data['laptop_branch__location'])
            response['laptop_branch']['datasets'][0]['data'].append(data['total'])
        
        laptop_assigned_data = Laptop.objects.aggregate(
            unassigned=Count('id', filter=Q(emp_id__isnull=True)),
            assigned=Count('id', filter=Q(emp_id__isnull=False))
        )
        response['laptop_availability']['labels'] = list(laptop_assigned_data.keys())
        response['laptop_availability']['datasets'][0]['data'] = list(laptop_assigned_data.values())

        current_year = datetime.now().year
        three_years_before = current_year - 3
        five_years_before = current_year - 5
        all_laptops = Laptop.objects.all()
        laptops_less_than_year = all_laptops.filter(
            laptop_date_purchased__year=current_year # = 2023
        ).count()
        laptops_between_year_and_three = all_laptops.filter(
            laptop_date_purchased__year__gte=three_years_before,
            laptop_date_purchased__year__lt=current_year
        ).count()
        laptops_between_three_and_five = all_laptops.filter(
            laptop_date_purchased__year__gte=five_years_before,
            laptop_date_purchased__year__lt=three_years_before
        ).count()
        laptops_greater_than_five = all_laptops.filter(
            laptop_date_purchased__year__lt=five_years_before
        ).count()
        response['laptop_age']['labels'] = ['< 1Y', '1-3Y', '3-5Y', '>5Y']
        response['laptop_age']['datasets'][0]['data'] = [
            laptops_less_than_year, laptops_between_year_and_three, laptops_between_three_and_five, laptops_greater_than_five
        ]
        return Response(response)