from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from specialists.forms import SpecialistForm
from specialists.models import Specialist, Dict, DictObj


def index(request):
    all_spec = Specialist.objects.order_by('surname')
    return render(request, 'list.html', {'all_spec': all_spec})


def estimate(request, spec_id):
    spec = get_object_or_404(Specialist, id=spec_id)
    my_dict = get_object_or_404(Dict, id=spec_id)
    estims = my_dict.items()
    main_value = 0
    if estims:
        main_value = spec.qualif(my_dict.getRealDict(), spec.setRanks(), spec.maxQualif(spec.setRanks()))
        main_value = round(main_value, 3)
    return render(request, 'estimate.html', {'spec': spec, 'estims': estims, 'main_value': main_value})


def spec_new(request):
    if request.method == "POST":
        form = SpecialistForm(request.POST)
        if form.is_valid():
            spec = form.save(commit=False)
            spec.save()
            dict = Dict(id=spec.id, spec=spec, dictName=("Оценки " + spec.surname))
            dict.save()
            return redirect('specialists:estimate', spec.id)
    else:
        form = SpecialistForm()

    return render(request, 'spec_new.html', {'form': form})


def spec_edit(request, spec_id):
    spec = get_object_or_404(Specialist, id=spec_id)
    if request.method == "POST":
        form = SpecialistForm(request.POST, instance=spec)
        if form.is_valid():
            spec = form.save(commit=False)
            spec.save()
            return redirect('specialists:estimate', spec.id)
    else:
        form = SpecialistForm(instance=spec)
    return render(request, 'spec_edit.html', {'form': form})


def estim_edit(request, spec_id):
    spec = get_object_or_404(Specialist, id=spec_id)
    my_dict = Dict(id=spec.id, spec=spec, dictName=("Оценки " + spec.surname))
    my_dict.save()

    if my_dict.__len__() == 12:
        my_dict.clear()
    estims = spec.setMarks()
    for est in estims:
        dict_obj = DictObj(container=my_dict, key=est, value=estims[est])
        dict_obj.save()
    return redirect('specialists:estimate', spec.id)


def spec_delete(request, spec_id):
    spec = get_object_or_404(Specialist, id=spec_id)
    spec.delete()
    return HttpResponseRedirect("/")
