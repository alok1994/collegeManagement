from django.shortcuts import render, get_object_or_404, redirect
from .models import Semester
from .forms import SemesterFeeUpdateForm

def fee_structure(request):
    semesters = Semester.objects.all()
    
    context = {'semesters': semesters}
    return render(request, 'fee_structure/fee_structure.html', context)

def update_semester_fee(request, semester_number):
    semester = get_object_or_404(Semester, semester_number=semester_number)
    if request.method == 'POST':
        form = SemesterFeeUpdateForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            return redirect('fee_structure')
    else:
        form = SemesterFeeUpdateForm(instance=semester)
    return render(request, 'fee_structure/update_semester_fee.html', {'form': form, 'semester': semester})
