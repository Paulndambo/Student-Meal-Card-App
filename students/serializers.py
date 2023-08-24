from rest_framework import serializers
from students.models import Student, DailyQuota, StudentExpediture, MealCard, Claim
from rest_framework import status
import datetime
from rest_framework.response import Response

class StudentSerializer(serializers.ModelSerializer):
    #expenditures = serializers.SerializerMethodField()
    #quotas = serializers.SerializerMethodField()
    amount_spent_today = serializers.SerializerMethodField()
    balance_today = serializers.SerializerMethodField()
    updated_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = "__all__"

    
    def get_updated_name(self, instance):
        new_name = self.context["request"].query_params.get("individual")
        
        return new_name

    """
    def get_expenditures(self, obj):
        return obj.student_expediture.all().values()

    
    def get_quotas(self, obj):
        return obj.student_quotas.all().values()

    """

    def get_amount_spent_today(self, obj):
        amount_spent = obj.student_quotas.order_by("-created").values_list('amount_spent', flat=True).first()
        return amount_spent

    def get_balance_today(self, obj):
        return obj.student_quotas.order_by("-created").values_list('balance', flat=True).first()


class StudentExpeditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentExpediture
        fields = "__all__"


    def create(self, validated_data):
       
        #=> When a student makes an expenditure, subtract/update the student quota balance

        #=: get specific quota expenditures to be able to update balances
     
        quota = validated_data["daily_quota"]
        quota_expenditures = sum(list(quota.quota_expeditures.all().values_list("amount_spent", flat=True)))
        total_quota_expenditures = quota_expenditures + validated_data["amount_spent"]

        print(f"Quota Expenditues: {total_quota_expenditures}")

        # Check if quota exceeded
        if total_quota_expenditures > quota.allocated_amount:
            #return Response({"failed": "You have exceeded your daily alocation"}, status=status.HTTP_400_BAD_REQUEST)
            raise serializers.ValidationError("Quota exceeded maximum allocated per day")
        
        quota.balance = quota.allocated_amount - total_quota_expenditures
        quota.amount_spent = total_quota_expenditures #quota.amount_spent + validated_data["amount_spent"]
        quota.save()
    
        print(f"Quota: {quota}")
        print(f"Validated Data: {validated_data}")

        return StudentExpediture.objects.create(**validated_data)
   
        

class StudentDailyQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyQuota
        fields = "__all__"



class MealCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealCard
        fields = "__all__"


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"