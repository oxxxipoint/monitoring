import random

from django.db import models


class Specialist(models.Model):
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50)
    birth = models.DateField('Дата рождения')

    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    def qualif(self, estims, ranks, maxQ):
        print(estims, ranks, sep='\n')
        sum = 0
        for rank in ranks:
            sum += float(ranks[rank]) * float(estims[rank])
        return sum / maxQ

    def setMarks(self):
        file = open('specialists/static/criteria/estimations.txt', 'r')
        marks = file.read()
        file.close()
        nums = [0, 0.25, 0.5, 0.75, 1]
        estims = {}
        for mark in marks.split('\n'):
            if mark != '' and not mark.isspace():
                estims[mark] = random.choice(nums)
        return estims

    def setRanks(self):
        file = open('specialists/static/criteria/coefficients.txt', 'r')
        file_text = file.read()
        file.close()
        ranks = {}
        for line in file_text.split('\n'):
            for word in line.split(' - '):
                if '.' in word:
                    ranks[line.split(' - ')[0]] = float(word)
        return ranks

    def maxQualif(self, ranks):
        return sum(ranks.values())

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'


class Dict(models.Model):
    spec = models.OneToOneField(Specialist, on_delete=models.CASCADE)
    dictName = models.CharField(max_length=240)

    def __str__(self):
        return self.dictName

    @staticmethod
    def getDict(name):
        df = Dict.objects.select_related().get(dictName=name)
        return df

    def __getitem__(self, key):
        return self.dictobj_set.get(key=key).value

    def __len__(self):
        return self.dictobj_set.count()

    def getRealDict(self):
        real_dict = {}
        for kvp in self.dictobj_set.all():
            real_dict[kvp.key] = kvp.value

        return real_dict

    def items(self):
        return [(kvp.key, kvp.value) for kvp in self.dictobj_set.all()]

    def clear(self):
        return self.dictobj_set.all().delete()

    class Meta:
        verbose_name = "Словарь"
        verbose_name_plural = "Словари"


class DictObj(models.Model):
    container = models.ForeignKey(Dict, db_index=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=240, db_index=True)
    value = models.CharField(max_length=240, db_index=True)

    def __str__(self):
        return "Оценка " + self.key

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
