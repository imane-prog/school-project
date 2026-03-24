from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.http import HttpResponse 
from .models import Student, Parent 
 
def student_list(request):
    students = Student.objects.all()
    print(f"DEBUG - Nombre d'étudiants envoyés au template: {students.count()}")  # Vérification
    return render(request, 'students/students.html', {'students': students})
 
def add_student(request): 
    if request.method == 'POST': 
        # Récupérer les données de l'étudiant 
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        student_id = request.POST.get('student_id') 
        gender = request.POST.get('gender') 
        date_of_birth = request.POST.get('date_of_birth') 
        student_class = request.POST.get('student_class') 
        joining_date = request.POST.get('joining_date') 
        mobile_number = request.POST.get('mobile_number') 
        admission_number = request.POST.get('admission_number') 
        section = request.POST.get('section') 
        student_image = request.FILES.get('student_image') 
 
        # Récupérer les données du parent 
        father_name = request.POST.get('father_name') 
        father_occupation = request.POST.get('father_occupation') 
        father_mobile = request.POST.get('father_mobile') 
        father_email = request.POST.get('father_email') 
        mother_name = request.POST.get('mother_name') 
        mother_occupation = request.POST.get('mother_occupation') 
        mother_mobile = request.POST.get('mother_mobile') 
        mother_email = request.POST.get('mother_email') 
        present_address = request.POST.get('present_address') 
        permanent_address = request.POST.get('permanent_address')

        try:
            # 1. Créer et sauvegarder le parent
            parent = Parent.objects.create(
                father_name=father_name,
                father_occupation=father_occupation,
                father_mobile=father_mobile,
                father_email=father_email,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                mother_mobile=mother_mobile,
                mother_email=mother_email,
                present_address=present_address,
                permanent_address=permanent_address
            )
            
            # 2. Créer l'étudiant lié au parent
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                gender=gender,
                date_of_birth=date_of_birth,
                student_class=student_class,
                joining_date=joining_date,
                mobile_number=mobile_number,
                admission_number=admission_number,
                section=section,
                student_image=student_image,
                parent=parent
            )
            
            messages.success(request, f'Étudiant {first_name} {last_name} ajouté avec succès !')
            return redirect('student_list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout : {str(e)}')
            return render(request, 'students/add-student.html')
    
    # GET request - afficher le formulaire vide
    return render(request, 'students/add-student.html') 
 
def view_student(request, student_id):
    """Affiche les détails d'un étudiant"""
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'students/student-details.html', {'student': student})

def edit_student(request, student_id):
    """Modifie les informations d'un étudiant existant"""
    student = get_object_or_404(Student, student_id=student_id)
    parent = student.parent
    
    if request.method == 'POST':
        # Récuperation  les informations de l'étudiant
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        student.joining_date = request.POST.get('joining_date')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        
        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')
        
        # Récuperation  les informations du parent
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')
        
        try:
            student.save()
            parent.save()
            messages.success(request, f'Étudiant {student.first_name} {student.last_name} modifié avec succès !')
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
    
    return render(request, 'students/edit-student.html', {'student': student, 'parent': parent})

def delete_student(request, student_id):
    """Supprime un étudiant et son parent associé"""
    student = get_object_or_404(Student, student_id=student_id)
    student_name = f"{student.first_name} {student.last_name}"
    
    if request.method == 'POST':
        try:
            student.delete()
            messages.success(request, f'Étudiant {student_name} supprimé avec succès !')
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        return redirect('student_list')
    
    return render(request, 'students/confirm-delete.html', {'student': student})
def student_dashboard(request):
    """Affiche le tableau de bord des étudiants"""
    students = Student.objects.all()
    total_students = students.count()
    return render(request, 'students/student-dashboard.html', {
        'students': students,
        'total_students': total_students,
    })

# @login_required(login_url='login')
def teacher_dashboard(request):
    """Affiche le tableau de bord pour les enseignants"""
    # Récupérer tous les étudiants
    students = Student.objects.all()
    total_students = students.count()
    total_classes = Student.objects.values('student_class').distinct().count()
    
    # Derniers étudiants ajoutés
    recent_students = students.order_by('-id')[:5]
    
    context = {
        'total_students': total_students,
        'total_classes': total_classes,
        'recent_students': recent_students,
        'teacher_name': request.user.get_full_name() if request.user.is_authenticated else 'Teacher',
    }
    
    return render(request, 'students/teacher-dashboard.html', context)