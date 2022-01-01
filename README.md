# photodatabase_longpolling_api
 
### Для работы с сервером

Создайте config.json файл со следующим содержанием:

```json
{
    "DBPASSWORD" : "yourpassword"
}
```

В данном репозитории храниться серверная часть проекта `photodatabase`. 
*Главный спонсор данного проекта: Человеческое любопытство.* 
Вы можете ознакомиться с внешней частью частью проекта по ссылке ниже.
https://github.com/meg4cyberc4t/photodatabase

#### Небольшие кадры из проекта
![flutter_06](/assets/flutter_06.png)
![flutter_02](/assets/flutter_02.png)
![flutter_03](/assets/flutter_03.png)
![flutter_04](/assets/flutter_04.png)
![flutter_08](/assets/flutter_08.png)
![flutter_10](/assets/flutter_10.png)

#### Этим проектом я хотел опробовать следующие пункты:

**Flutter Web**
До этого я работал с Flutter только как разработка мобильных приложений.
Можно сказать, что структура самого приложения примерно одинаковая, но есть нативные трудности. Так, например, очень сильно усложняется работа с файлами, поскольку `dart:io` не работает в Web.
Важно уточнить, что я не опробовал весь Web, а лишь малую часть. Мне очень хочется поработать с html и попробовать использовать dart как конкурент javascript, но уже в следующих проектах...)

**Longpolling API**
Интересно было реализовать longpolling в рамках Python и базовых инструментов программирования. 
Важная ремарка: на обоих сторонах разработки LP был реализован "колхозным" и максимально понятным методом. 
Так же стоит обратить внимание, что нет идеального метода для получения данных. В этом приложении websocket был бы куда эффективнее, но с ним эксперименты уже проводил. Абстрагируйтесь от своей ситуации, количестве и частоте данных.

**Multithreaded asynchronous flask**
Очень большая часть времени ушла на реализацию работы с базой данных в асинхронном режиме. Мне не понравилось. Для таких прототипов flask удобен, но использование его в серьёзных коммерческих целях я не вижу.