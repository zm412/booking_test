
document.addEventListener('DOMContentLoaded', function() {
    let calendar = document.querySelector('#calendar')
  if(calendar) createCalendar(calendar, 2021, 11);
  for(let elem of document.querySelectorAll('.td_class')){
    elem.onclick = (e) => e.target.classList.toggle('green')
  }
})

function formatDate(date) {
  var dd = date.getDate();
  if (dd < 10) dd = '0' + dd;
  var mm = date.getMonth() + 1;
  if (mm < 10) mm = '0' + mm;
  var yy = date.getFullYear() % 100;
  if (yy < 10) yy = '0' + yy;
  return dd + '.' + mm + '.' + yy;
}

 function createCalendar(elem, year, month) {

      let mon = month - 1; 
      let d = new Date(year, mon);
      

      let table = '<table><tr><th>пн</th><th>вт</th><th>ср</th><th>чт</th><th>пт</th><th>сб</th><th>вс</th></tr><tr>';

      for (let i = 0; i < getDay(d); i++) {
        table += '<td></td>';
      }
      while (d.getMonth() == mon) {

        console.log(formatDate(d), 'd')
        table += `<td data-book=${formatDate(d)} class="td_class">` + d.getDate() + '</td>';

        if (getDay(d) % 7 == 6) { 
          table += '</tr><tr>';
        }

        d.setDate(d.getDate() + 1);
      }

      if (getDay(d) != 0) {
        for (let i = getDay(d); i < 7; i++) {
          table += '<td></td>';
        }
      }

      table += '</tr></table>';

      elem.innerHTML = table;
    }

    function getDay(date) {
      let day = date.getDay();
      if (day == 0) day = 7; 
      return day - 1;
    }


