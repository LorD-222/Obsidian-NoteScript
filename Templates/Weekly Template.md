<%tp.file.rename("Еженедельная заметка") /* I have to do this for some reason because it wont let me name normally for whatever reason, this fixed the bug*/%>
## 📅 За неделю

### 📊 Результаты

<%*
folder = tp.file.folder(relative=true)
const weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
const weekdayLabels = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

// Get year and week from folder path
const pathParts = folder.split('/');
const year = pathParts[1];  // Assumes year is the second part of the path
const week = pathParts[2];  // Assumes week is the third part of the path

// Check each day of the week
for (let i = 0; i < 7; i++) {  
	day = weekday[i]
	dayLabels = weekdayLabels[i]

	// Get day number based on year and week
	dayNo = tp.date.weekday("DD", i, `${year}${week.padStart(2, "0")}`, "YYYYww")

	tR += `#### ${dayLabels}\n`;
	tR += `![[${folder}/${dayNo}-${day}# Задачи на сегодня]]\n\n`;
}

%>

### 📈 Еженедельная статистика
```dataviewjs

```

```dataviewjs
const folder = "<%tp.file.folder(relative=true)%>"
const weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
const weekdayLabels = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
// doing things in a very roundabout way because templater is being uncooperative
const year = folder.split('/').slice(1, 2).join('/');
const week = parseInt((folder.split('/').slice(2, 3).join('/')).slice(-1));



var one = undefined;
dayNo = "03"
one = dv.page(folder.concat("/", dayNo.concat("-", weekday[0])));
if (one==undefined) { one = 0; }

var two = undefined;
dayNo = "04"
two = dv.page(folder.concat("/", dayNo.concat("-", weekday[1])));
if (two==undefined) { two = 0; }

var thr = undefined;
dayNo = "05"
thr = dv.page(folder.concat("/", dayNo.concat("-", weekday[2])));
if (thr==undefined) { thr = 0; }

var fou = undefined;
dayNo = "06"
fou = dv.page(folder.concat("/", dayNo.concat("-", weekday[3])));
if (fou==undefined) { fou = 0; }

var fiv = undefined;
dayNo = "07"
fiv = dv.page(folder.concat("/", dayNo.concat("-", weekday[4])));
if (fiv==undefined) { fiv = 0; }

var six = undefined;
dayNo = "08"
six = dv.page(folder.concat("/", dayNo.concat("-", weekday[5])));
if (six==undefined) { six = 0; }

var sev = undefined;
dayNo = "09"
sev = dv.page(folder.concat("/", dayNo.concat("-", weekday[6])));
if (sev==undefined) { sev = 0; }

const chartData = {
    type: 'line',
    data: {
        labels: weekdayLabels,
        datasets: [{
            label: "Счастье",
            data: [one.Happiness, two.Happiness, thr.Happiness, fou.Happiness, fiv.Happiness, six.Happiness, sev.Happiness],
            backgroundColor: 'rgba(50, 205, 50, 0.2)',
            borderColor: 'rgba(50, 205, 50, 1)',
            borderWidth: 1,
			fill: false,
			tension: 0.2
        },	{
			label: "Стресс",
			data: [one["Stress"], two["Stress"], thr["Stress"], fou["Stress"], fiv["Stress"], six["Stress"], sev["Stress"]],
			backgroundColor: 'rgba(220, 20, 60, 0.2)',
            borderColor: 'rgba(220, 20, 60, 1)',
            borderWidth: 1,
			fill: false,
			tension: 0.2
		}, {
			label: "Производительность",
			data: [one.Productivity, two.Productivity, thr.Productivity, fou.Productivity, fiv.Productivity, six.Productivity, sev.Productivity],
			backgroundColor: 'rgba(255, 165, 0, 0.2)',
            borderColor: 'rgba(255, 165, 0, 1)',
            borderWidth: 1,
			fill: false,
			tension: 0.2
		}, {
			label: "Здоровье",
			data: [one.Health, two.Health, thr.Health, fou.Health, fiv.Health, six.Health, sev.Health],
			backgroundColor: 'rgba(148, 0, 211, 0.2)',
            borderColor: 'rgba(148, 0, 211, 1)',
            borderWidth: 1,
			fill: false,
			tension: 0.2
		}],
    },
	options: {
		scales: {
		    y: {
		        min: 0,
		        max: 10,
			}
	    }
	}
}
const chartData1 = {
    type: 'line',
    data: {
        labels: weekdayLabels,
        datasets: [{
			label: "Часы работы",
			data: [one["Work Time"], two["Work Time"], thr["Work Time"], fou["Work Time"], fiv["Work Time"], six["Work Time"], sev["Work Time"]],
			backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
			fill: false,
			tension: 0.2
		}, {
			label: "Часы сна",
			data: [one["Sleep Time"], two["Sleep Time"], thr["Sleep Time"], fou["Sleep Time"], fiv["Sleep Time"], six["Sleep Time"], sev["Sleep Time"]],
			backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
			fill: false,
			tension: 0.2
		}, {
			label: "Время на обучение",
			data: [one["Learning Time"], two["Learning Time"], thr["Learning Time"], fou["Learning Time"], fiv["Learning Time"], six["Learning Time"], sev["Learning Time"]],
			backgroundColor: 'rgba(255, 206, 86, 0.2)',
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1,
			fill: false,
			tension: 0.2
		}, {
			label: "Физическая активность",
			data: [one["Physical Activity"], two["Physical Activity"], thr["Physical Activity"], fou["Physical Activity"], fiv["Physical Activity"], six["Physical Activity"], sev["Physical Activity"]],
			backgroundColor: 'rgba(30, 144, 255, 0.2)',
            borderColor: 'rgba(30, 144, 255, 1)',
            borderWidth: 1,
			fill: false,
			tension: 0.2
		}],
    },
	options: {
		scales: {
		    y: {
		        min: 0,
		        max: 10,
			}
	    }
	}
}
window.renderChart(chartData, this.container);
window.renderChart(chartData1, this.container);
```
