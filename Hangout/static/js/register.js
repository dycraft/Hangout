var fixTimes = [];
var tds = $("td");
for (var i = 0; i < 28; i++) {
    fixTimes.push(0);
}

function selectDate(value) {
    if (value >= 0 && value < 28) {
        fixTimes[value] = 1 - fixTimes[value];
    }

    if (fixTimes[value] === 1) {
        tds[value].style.backgroundColor = '#FFF';
    } else {
        tds[value].style.backgroundColor = '#EBEBEB';
    }
}

function getFixTime() {
    var result = 0;
    for (var i = 0; i < 28; i++) {
        result = result * 2 + fixTimes[i];
    }
    return result;
}
