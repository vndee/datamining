from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from datamining.forms import InputForm
from datamining.tree import DTree
from datamining.rule import AssociationRule

dtree = DTree()
assoc = AssociationRule()


def parse_request(post):
    data = []
    data.append(post['age'])
    data.append(post['sex'])
    data.append(post['cp'])
    data.append(post['trestbps'])
    data.append(post['chol'])
    data.append(post['fbs'])
    data.append(post['restecg'])
    data.append(post['thalach'])
    data.append(post['exang'])
    data.append(post['oldpeak'])
    data.append(post['slope'])
    data.append(post['ca'])
    data.append(post['thal'])
    return data


class Home(TemplateView):
    template_name = 'home.html'


def association_rule(request):
    context = {}
    if request.method == 'POST':
        # data = parse_request(request.POST)
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        file_name = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.location + '/' + file_name

        assoc.data = assoc.load_data(uploaded_file_url)
        assoc.exc_cal_ls_max_itemset()
        assoc.get_ls_assoc()

        context['item_set'] = assoc.ls_max_itemset
        context['assoc'] = assoc.ls_assoc

        return render(request, 'associationrule.html', context)

    return render(request, 'associationrule.html', context)


def decision_tree(request):
    context = {}
    if request.method == 'POST':
        data = parse_request(request.POST)
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        file_name = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.location + '/' + file_name

        dtree.load_data(uploaded_file_url)
        dtree.training()
        tr_acc, te_acc = dtree.validate()

        context['tr_acc'] = tr_acc
        context['te_acc'] = te_acc
        context['pred'] = dtree.predict([data])[0]

        return render(request, 'decisiontree.html', context)

    return render(request, 'decisiontree.html', context)