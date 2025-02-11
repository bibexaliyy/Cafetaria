import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cafeteria.models import Student, Meal, MealTransaction,AdminRole
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def home(request):
    return HttpResponse("Welcome to the Cafeteria System!")


def authenticate_fingerprint(request):
    """Simulate fingerprint authentication (Replace with real fingerprint logic)"""
    fingerprint_id = request.POST.get("fingerprint_id")
    
    if not fingerprint_id:
        return JsonResponse({"success": False, "error": "Fingerprint ID required"}, status=400)

    try:
        student = Student.objects.get(fingerprint_id=fingerprint_id)
        return JsonResponse({
            "success": True,
            "student": {
                "id": student.id,
                "name": student.user.username,
                "meal_balance": student.meal_balance
            }
        })
    except Student.DoesNotExist:
        return JsonResponse({"success": False, "error": "Student not found"}, status=404)


def get_meals(request):
    """Fetch all available meals"""
    meal_type = request.GET.get("meal_type")  # Optional filter
    
    meals_query = Meal.objects.all()
    if meal_type:
        meals_query = meals_query.filter(meal_type=meal_type)

    meals = list(meals_query.values("id", "name", "meal_type", "available_options"))
    return JsonResponse({"meals": meals})


@csrf_exempt  
def select_meal(request):
    """Student selects a meal, and it updates their meal balance"""
    student_id = request.POST.get("student_id")
    meal_id = request.POST.get("meal_id")

    if not student_id or not meal_id:
        return JsonResponse({"success": False, "error": "Student ID and Meal ID required"}, status=400)

    try:
        student = Student.objects.get(id=student_id)
        meal = Meal.objects.get(id=meal_id)

        if student.meal_balance <= 0:
            return JsonResponse({"success": False, "error": "No meals remaining"}, status=403)

        student.meal_balance -= 1
        student.save()

        
        MealTransaction.objects.create(student=student, meal=meal)
        return JsonResponse({
            "success": True,
            "message": f"{student.user.username} collected {meal.name}",
            "remaining_meals": student.meal_balance
        })
    except Student.DoesNotExist:
        return JsonResponse({"success": False, "error": "Student not found"}, status=404)
    except Meal.DoesNotExist:
        return JsonResponse({"success": False, "error": "Meal not found"}, status=404)

def generate_meal_ticket(request, ticket_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="meal_ticket_{ticket_id}.pdf"'
    
    pdf_path = f'meal_ticket_{ticket_id}.pdf'
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Meal Ticket ID: {ticket_id}")
    p.drawString(100, 730, "Valid for: One Meal")
    p.drawString(100, 710, "Cafeteria System")

    p.showPage()
    p.save()
    
    os.startfile(pdf_path, "print")

    return response

def get_audit_report(request):
    """ Generate a monthly report of meals consumed """
    report = MealTransaction.objects.values("student__user__username").annotate(total_meals=models.Count("id"))
    return JsonResponse(list(report), safe=False)
