
let current_mode = 'view';
let time_object = {
  parking_lot: [null],
  dates_set:[]
};

document.addEventListener('DOMContentLoaded', function() {
  let calendar = document.querySelector('#calendar');
  let reservation = document.querySelector('#reservation');
  let my_booking = document.querySelector('#my_booking');
  let hours = document.querySelector('#hours');
  let form_r = document.querySelector('#form_r');
  form_r.addEventListener('submit', send_info)

  fetchDataGet();
  if(calendar){
    createCalendar(calendar, 2021, 10);
    time_object['parking_lot'] = calendar.dataset.lot;
  } 
  

  for(let elem of document.querySelectorAll('.td_class')){
    elem.addEventListener('click', open_booking);

      function open_booking(){
        add_day(hours, document.querySelectorAll('.td_class'), elem, reservation);
        this.removeEventListener('click', open_booking);
        this.addEventListener('click', close_booking);
      }

      function close_booking(){
        remove_day(hours, document.querySelectorAll('.td_class'), elem, reservation);
        this.removeEventListener('click', close_booking);
        this.addEventListener('click', open_booking);
      }
  }
  let inp = document.querySelector('#mode');
  inp.onchange = (e) => {
    current_mode =  e.target.checked ? 'booking' : 'view';
  }
  
})

function send_info(e){
  e.preventDefault();
  console.log(e.target, 'target')
  console.log(time_object, 'res')
  fetchDataPost('/book_parking/', time_object)
    .then(result => { 
      console.log(result)
    })
 
}

async function fetchDataGet() {
    try {
      const response = await fetch('/get_all_hours/');
      const json = await response.json();
      console.log(json, 'sjon')
    } catch (e) {
        console.error(e);
    }
};

async function fetchDataPost(url, obj){  
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  try{
    let response = await fetch(url, {
      method: 'POST',
      headers: { 
        'X-CSRFToken': csrftoken,
        "Content-type": "application/json"
      },
      body: JSON.stringify(obj) 
    });
    return await response.json();
  } catch(e){
    console.error(e);
  }
}


function reservation_info(dayD){
  let reservation = document.querySelector('#reservation');
  let arr = time_object[dayD];
  let str = arr && arr.length > 0 ? `reservation time: ${dayD} - ${ arr.join(', ') }` : '';
  if(li=document.getElementById(dayD)){
   li.innerHTML =  str;
  }else{
    let li = createEl('li', reservation, {id: dayD}, str)
    reservation.appendChild(li);
  }
}


function remove_day(hours, elems, current_elem, message_elem){
  let arr = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17' ]
  current_elem.classList.remove('green');
  hours.innerHTML = '';
  let arr_collection = time_object[current_elem.dataset.book]
  for(let elem of arr){
    if(arr_collection.indexOf(elem) != -1){
      let index = arr_collection.indexOf(elem);
      arr_collection.splice(index, 1);
    }
    if(arr_collection.length == 0){
      let index = time_object['dates_set'].indexOf(current_elem.dataset.book);
      time_object['dates_set'].splice(index, 1);
    }
  }

  if(arr_collection){
    let li = document.getElementById(current_elem.dataset.book)
    if(li) message_elem.removeChild(li);
  }
  console.log(time_object, '2')
}

function add_day(hours, elems, current_elem, message_elem){
  hours.innerHTML = '';
  if(current_mode == 'booking'){
    current_elem.classList.add('green');
    time_object[current_elem.dataset.book] = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17'] ;
    let index = time_object['dates_set'].indexOf(current_elem.dataset.book);
    if(index == -1) time_object['dates_set'].push(current_elem.dataset.book);
    reservation_info(current_elem.dataset.book);
  } 

  console.log(time_object, '2')
  for(let el of elems){
    current_elem == el ?  el.classList.add('active_day') :  el.classList.remove('active_day')
  }
  create_hours_tbl(hours, current_elem.dataset.book, current_elem);
}


function add_hour(hour_elem, date, message_elem){
  hour_elem.classList.add('hours_green');
  time_object[date] ?  time_object[date].push(hour_elem.id) : time_object[date] = [hour_elem.id] ;
  reservation_info(date);
  console.log(time_object, '3')
}

function remove_hour(hour_elem, date, parent_day, message_elem){
  hour_elem.classList.remove('hours_green');

  let index = time_object[date].indexOf(hour_elem.id);
  time_object[date].splice(index, 1);
  
  let arr = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17' ]
  if(( hour_elem.id ) >= 8 && hour_elem.id <= 17){
    parent_day.classList.remove('green');
    parent_day.classList.add('blue_day');
  }

  if(time_object[date].length == 0){
    parent_day.classList.remove('blue_day');
    delete time_object[date]
    let index = time_object['dates_set'].indexOf(date);
    time_object['dates_set'].splice(index, 1);
  }

  reservation_info(date);
  console.log(time_object, '3')
}

function create_hours_tbl(par, date, parent_day){
  let title = `<h1>${date}</h1>`
  let hours_tbl = title + '<table id="hours_t"><tr>'
  for(let i = 0; i < 24; i++){
    let classN = i >= 8 && i <= 17 && current_mode == 'booking' ? 'hours_class hours_green' : 'hours_class';
    if(i < 10){
      hours_tbl +=`<td id='0${i}' class="${classN}">0${i}:00</td>`
    }else{
      hours_tbl +=`<td id='${i}' class="${classN}">${i}:00</td>`
    }
  }
  hours_tbl += '</tr></table>'
  par.insertAdjacentHTML('afterbegin', hours_tbl)

  let reservation = document.querySelector('#reservation');
  if(current_mode == 'booking'){
    for(let elem of document.querySelectorAll('.hours_class')){

      if(!elem.classList.contains('hours_green')){
        elem.addEventListener('click',  add_hours_action);
      }else{
        elem.addEventListener('click',  remove_hours_action);
      }

      function add_hours_action(){
        add_hour(elem, date, );
        this.removeEventListener('click', add_hours_action);
        this.addEventListener('click', remove_hours_action);
      }

      function remove_hours_action(){
        remove_hour(elem, date, parent_day);
        this.removeEventListener('click', remove_hours_action);
        this.addEventListener('click', add_hours_action);
      }
    }
  }

}




function formatDate(date) {
  var dd = date.getDate();
  if (dd < 10) dd = '0' + dd;
  var mm = date.getMonth() + 1;
  if (mm < 10) mm = '0' + mm;
  var yy = date.getFullYear();
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


