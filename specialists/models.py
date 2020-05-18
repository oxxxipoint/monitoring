from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def qualif(estims, ranks, maxQ):
    sum = 0
    for rank in ranks:
        if estims.get(str(rank)):
            sum += float(ranks[rank]) * float(estims[str(rank)])
    return sum / maxQ


def maxQualif(ranks):
    return float(sum(ranks))


class Specialist(models.Model):
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50)
    birth = models.DateField('Дата рождения')
    main_estim = models.DecimalField(max_digits=4, decimal_places=3, default=0)

    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

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


class Criteria(models.Model):
    criteria_name = models.CharField('Имя критерия', max_length=50, db_index=True, primary_key=True)
    criteria_value = models.DecimalField('Вес критерия', max_digits=2, decimal_places=1,
                                         validators=[MinValueValidator(0), MaxValueValidator(1)])


    @classmethod
    def setRanks(cls):
        dir = 'coeff/coefficients.txt'
        file = open(dir, 'r')
        file_text = file.read()
        file.close()
        ranks = {}
        for line in file_text.split('\n'):
            for word in line.split(' - '):
                if '.' in word:
                    ranks[line.split(' - ')[0]] = float(word)
        return ranks

    def __str__(self):
        return self.criteria_name

    class Meta:
        verbose_name = "Критерий"
        verbose_name_plural = "Критерии"


class DictObj(models.Model):
    zero = '0'
    one = '0.25'
    two = '0.5'
    three = '0.75'
    four = '1.0'

    VALUES = [(zero, 0),
              (one, 0.25),
              (two, 0.5),
              (three, 0.75),
              (four, 1.0)]
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE, verbose_name='Критерий')
    container = models.ForeignKey(Dict, db_index=True, on_delete=models.CASCADE)
    key = models.CharField('Имя критерия', max_length=50, db_index=True)
    value = models.CharField('Уровень владения', max_length=10, choices=VALUES, default=0)

    def __str__(self):
        return "Оценка " + self.key

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
