
let current_mode = 'view';
let time_object = {};

document.addEventListener('DOMContentLoaded', function() {
  let calendar = document.querySelector('#calendar');
  let reservation = document.querySelector('#reservation');
  let hours = document.querySelector('#hours');

  if(calendar) createCalendar(calendar, 2021, 10);

  for(let elem of document.querySelectorAll('.td_class')){
    elem.onclick = (e) =>{
      hours.innerHTML = '';
      if(current_mode == 'booking'){
        elem.classList.toggle('green');
        time_object[e.target.dataset.book] = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17'] ;
      } 
      for(let el of document.querySelectorAll('.td_class')){
        if(elem == el){
          el.classList.add('active_day');
        }else{
          el.classList.remove('active_day');
        }
      }
      create_hours_tbl(hours, elem.dataset.book, elem);
      let li = createEl('li', elem, {}, `reservation time: ${e.target.dataset.book}, 08.00 - 17.00`)
      reservation.appendChild(li);
    } 
  }

  let inp = document.querySelector('#mode');
  inp.onchange = (e) => {
    current_mode =  e.target.checked ? 'booking' : 'view';
  console.log(current_mode, 'mode')
  }
  
 
})

function create_hours_tbl(par, date, parent_day){
  let title = `<h1>${date}</h1>`
  let hours_tbl = title + '<table id="hours_t"><tr>'
  for(let i = 0; i < 24; i++){
    let classN = i >= 8 && i <= 17 && current_mode == 'booking' ? 'hours_class hours_green' : 'hours_class';
    console.log(classN, 'classN')
    if(i < 10){
      hours_tbl +=`<td id='0${i}' class="${classN}">0${i}:00</td>`
    }else{
      hours_tbl +=`<td id='${i}' class="${classN}">${i}:00</td>`
    }
  }
  hours_tbl += '</tr></table>'
  par.insertAdjacentHTML('afterbegin', hours_tbl)

  if(current_mode == 'booking'){
    for(let elem of document.querySelectorAll('.hours_class')){
      elem.onclick = (e) =>{
        elem.classList.toggle('hours_green');
        if(elem.id >= 8 && elem.id <=17){
          parent_day.classList.remove('green');
          parent_day.classList.add('blue_day');
        }
      } 
    }
  }

}




function formatDate(date) {
  var dd = date.getDate();
  if (dd < 10) dd = '0' + dd;
  var mm = date.getMonth() + 1;
  if (mm < 10) mm = '0' + mm;
  var yy = date.getFullYear() % 100;
  if (yy < 10) yy = '0' + yy;
  return dd + '.' + mm + '.' + yy;
}

function createCalendar(elem, year, month){
  let mon = month - 1; 
  let d = new Date(year, mon);
  let title = `<h1>${month}.${year}</h1>`
  let mode = `<label>Включить режим бронирования</label><input type='checkbox' id='mode' value='on'>`
  let table = title + mode +'<table><tr><th>пн</th><th>вт</th><th>ср</th><th>чт</th><th>пт</th><th>сб</th><th>вс</th></tr><tr>';
  for(let i = 0; i < getDay(d); i++){
    table += '<td></td>';
  }

  while(d.getMonth() == mon){
    table += `<td data-book=${formatDate(d)} class="td_class">` + d.getDate() + '</td>';
    if (getDay(d) % 7 == 6){ 
      table += '</tr><tr>';
    }
    d.setDate(d.getDate() + 1);
  }

  if(getDay(d) != 0){
    for (let i = getDay(d); i < 7; i++){
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


function createEl(tag, par, objAttr={}, inner=''){
  new_el = document.createElement(tag);
  for(key in objAttr){
    new_el.setAttribute(key, objAttr[key]);
  }
  new_el.innerHTML = inner;
  par.append(new_el);
  return new_el;
}


