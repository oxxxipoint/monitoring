import random

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from specialists.forms import SpecialistForm, DictObjForm, CriteriaForm
from specialists.models import Specialist, Dict, DictObj, Criteria


def index(request):
    all_spec = Specialist.objects.order_by('main_estim')
    return render(request, 'list.html', {'all_spec': all_spec})


def show_criteria(request):
    all_criteria = Criteria.objects.order_by('criteria_name')

    return render(request, 'criteria.html', {'all_criteria': all_criteria})


def new_criteria(request):
    if request.method == "POST":
        form = CriteriaForm(request.POST)
        if form.is_valid():
            crit = form.save(commit=False)
            crit.save()
            return redirect('specialists:show_criteria')
    else:
        form = CriteriaForm()

    return render(request, 'new_criteria.html', {'form': form})


def delete_criteria(request, criteria_name):
    criteria = get_object_or_404(Criteria, criteria_name=criteria_name)
    criteria.delete()
    return redirect('specialists:show_criteria')


def set_default(request):
    all_criteria = Criteria.objects.order_by('criteria_name')
    ranks = Criteria.setRanks()
    for rank in ranks:
        try:
            Criteria.objects.get(criteria_name=rank)
        except Criteria.DoesNotExist:
            crit = Criteria(criteria_name=rank, criteria_value=ranks[rank])
            crit.save()

    return render(request, 'criteria.html', {'all_criteria': all_criteria})


def show_estimates(request, spec_id):
    spec = get_object_or_404(Specialist, id=spec_id)
    my_dict = get_object_or_404(Dict, id=spec_id)
    estims = my_dict.items()
    main_value = 0
    ranks = {}
    for crit in Criteria.objects.all():
        ranks[crit] = crit.criteria_value
    if estims:
        main_value = spec.qualif(my_dict.getRealDict(), ranks, spec.maxQualif(ranks.values()))
        main_value = round(main_value, 3)
        spec.main_estim = main_value
        spec.save()
    estims.sort()
    return render(request, 'estimate.html', {'spec': spec, 'estims': estims, 'main_value': main_value})


def set_random(request, spec_id):
    all_criteria = Criteria.objects.order_by('criteria_value')
    rates = [0, 0.25, 0.5, 0.75, 1]
    for criteria in all_criteria:
        try:
            DictObj.objects.get(container=get_object_or_404(Dict, id=spec_id), key=criteria.criteria_name)
        except DictObj.DoesNotExist:
            estim = DictObj(container=get_object_or_404(Dict, id=spec_id),
                            criteria_id=criteria.criteria_name,
                            key=criteria.criteria_name,
                            value=random.choice(rates))
            estim.save()
    return show_estimates(request, spec_id)


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
    try:
        Dict.objects.get(id=spec.id)
    except Dict.DoesNotExist:
        my_dict = Dict(id=spec.id, spec=spec, dictName=("Оценки " + spec.surname))
        my_dict.save()

    if request.method == "POST":
        form = DictObjForm(request.POST)
        if form.is_valid():
            estim = form.save(commit=False)
            estim.container = Dict.objects.get(id=spec.id)
            estim.key = estim.criteria.criteria_name
            estim.save()
            return redirect('specialists:estim_edit', spec.id)
    else:
        form = DictObjForm()

    return render(request, 'estim_edit.html', {'form': form, 'spec': spec})


def estim_delete(request, spec_id, estim_name):
    estim = get_object_or_404(DictObj, container=get_object_or_404(Dict, id=spec_id), key=estim_name)
    estim.delete()
    return redirect('specialists:estimate', spec_id)


def spec_delete(request, spec_id):
    spec = get_object_or_404(Specialist, id=spec_id)
    spec.delete()
    return HttpResponseRedirect("/")
