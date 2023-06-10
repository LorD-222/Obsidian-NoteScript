---
title: Daily
tags: [List]
---

# Daily

## Описание
Краткое описание темы или раздела.

## Список Заметок
```dataview
list from "Daily" 
where date(file.mtime) > date(today) - dur(1 month) 
limit 20
```

## Последние изменения
```dataview
table file.ctime as "Дата создания", file.mtime as "Дата последнего изменения" 
from "Daily" where date(file.mtime) > date(today) - dur(1 week) 
sort file.mtime desc
limit 10
```