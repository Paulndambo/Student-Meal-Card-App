from django.shortcuts import render
from .serializers import StudentSerializer, StudentExpeditureSerializer, ClaimSerializer, StudentDailyQuotaSerializer, MealCardSerializer
from rest_framework import viewsets, status, generics
from students.models import Student, StudentExpediture, DailyQuota, MealCard, Claim
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import datetime
from rest_framework.renderers import JSONRenderer
from rest_framework_csv.renderers import CSVRenderer
# Create your views here.
class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        individual = self.request.query_params.get("individual")
        #print(f"Values: {individual}")
        return self.queryset

    def get_context_data(self):
        return {"request": self.request}
    


class StudentExpeditureModelViewSet(viewsets.ModelViewSet):
    queryset = StudentExpediture.objects.all()
    serializer_class = StudentExpeditureSerializer


class StudentDailyQuotaModelViewSet(viewsets.ModelViewSet):
    queryset = DailyQuota.objects.all()
    serializer_class = StudentDailyQuotaSerializer


class MealCardModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MealCard.objects.all()
    serializer_class = MealCardSerializer

    def get_queryset(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return MealCard.objects.all()
        return "Hello World"


class ClaimModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    
    renderer_classes = [JSONRenderer, CSVRenderer]

    """
    def get_queryset(self):
        end_date_str = self.request.query_params.get("end_date")
        start_date_str = self.request.query_params.get("start_date")
        #print(f"Start Date: {start_date}, End Date: {end_date}")
        data = self.queryset
        if start_date_str and end_date_str:
            start_date_dt = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date_dt = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            print(start_date_dt, end_date_dt)
            queryset = self.queryset.filter(created__date__gte=start_date_dt).filter(created__date__lte=end_date_dt)
        else:
            queryset = self.queryset[:40]
        #for x in data:
        #    created = x.created.date()
        #    type_of = type(created)
        #    print(f"Created: {created}, {created > start_date_dt.date()}")

        #if start_date and end_date:
        #    queryset = self.queryset.filter(created__date__gte=start_date)
        return queryset
    """
