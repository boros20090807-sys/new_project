from django.db import models
from django.contrib.auth.models import User 

class Publisher(models.Model):
    title = models.CharField(max_length=200, verbose_name="Называние")
    description = models.TextField(verbose_name='Описание')

    class Meta:
            verbose_name = 'издатель'
            verbose_name_plural = 'издатели'
    def __str__(self):
            return self.title

class Games(models.Model):

    TYPE_GAMES = (
    ("Экшен","Action"),
    ( "Приключения" ,'Adventure'),
    ("Головоломки" ,"Puzzle")
    )
    
    PLATFORM = (
    ('PlayStation 5','PS'), 
    ('Xbox Series X','Xbox'),
    ('Computer','PC')
    )
    
    title = models.CharField(max_length=200, verbose_name="Называние")
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    type_games = models.CharField(max_length=50, choices=TYPE_GAMES, verbose_name="Тип игры")
    type_platform = models.CharField(max_length=50, choices=PLATFORM, verbose_name="Платформа")
    sezi=models.FloatField(verbose_name="Размер (ГБ)", default=0.0)
    year = models.IntegerField(verbose_name='Год выпуска')
    created_at = models.DateTimeField(auto_now_add = True)
    image = models.ImageField('Фотография', upload_to='posts/', blank=True, null=True)
    publisher= models.ForeignKey(Publisher,on_delete=models.CASCADE, related_name='requirements', verbose_name="Издатель", blank=True, null=True)
    

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'игры'
    def __str__(self):
        return self.title



class GamesReview(models.Model):

    GAMES_RAITING = (
        (1, '⭐️'),
        (2, '⭐️⭐️ '),
        (3, '⭐️⭐️⭐️'),
        (4, '⭐️⭐️⭐️⭐️'),
        (5, '⭐️⭐️⭐️⭐️⭐️'),
    )

    user=models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='review'
    )
    name = models.CharField(max_length= 200, verbose_name = "название")
    text = models. TextField( verbose_name = "OueHka")
    raiting = models.IntegerField(choices=GAMES_RAITING, verbose_name = "PenTnHr" )
    games = models.ForeignKey(Games,on_delete = models. CASCADE,related_name = 'review')
    created_at = models.DateTimeField(auto_now_add = True)

    game=models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        related_name='review'
        )


    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def str_ (self):
        return f'{self.name} - {self.games}'

class SystemRequirements(models.Model):
    game = models.OneToOneField(Games, on_delete=models.CASCADE, related_name='requirements', verbose_name="Игра")
    os = models.CharField(max_length=100, verbose_name="ОС", default="Windows 10/11")
    processor = models.CharField(max_length=150, verbose_name="Процессор")
    ram = models.CharField(max_length=50, verbose_name="Оперативная память")
    graphics = models.CharField(max_length=150, verbose_name="Видеокарта")
    storage = models.CharField(max_length=50, verbose_name="Место на диске")

    class Meta:
        verbose_name = 'Системные требования'
        verbose_name_plural = 'Системные требования'

    def __str__(self):
        return f"Требования для {self.game.title}"


