
let current_mode = 'view';
let time_object = {
  parking_lot: [null],
  dates_set:[]
};

let booking_info, my_bookings; 
let update_collection = {'day_id': null, 'lot':null, 'day': null, 'hours': [], 'original': []};
let data = new Date();
let cur_year = data.getFullYear();
let cur_month = data.getMonth();
let arr_temp = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17' ];

document.addEventListener('DOMContentLoaded', function() {
  let calendar = document.querySelector('#calendar');
  let start_info = document.querySelector('#start_info');
  let form_r = document.querySelector('#form_r');
  let inp = document.querySelector('#mode');
  let upd_sess = document.querySelectorAll('.upd_sess');
  console.log(upd_sess, 'sess')
  if(upd_sess) upd_sess.forEach(n => n.onclick= (e)=> upd_sess_func(booking_info,
                                                                    my_bookings,
                                                                    e.target.nextElementSibling, 
                                                                    e.target.dataset.day, 
                                                                    e.target.dataset.lot ))

  time_object['parking_lot'] = start_info.dataset.lot;
  time_object['user_id'] = start_info.dataset.user;
  console.log(calendar, 'calendar')

  if(form_r) form_r.addEventListener('submit', send_info);
  if(calendar) fetchDataGet(calendar);


  if(inp){
    inp.onchange = (e) => {
      current_mode =  e.target.checked ? 'booking' : 'view';
      console.log(current_mode, 'curMode')
      createCalendar(calendar, cur_year, cur_month);
    }
  }

})

function upd_sess_func(obj_common, obj_particular, elem, day, lot){
  console.log(obj_common, 'commont')
  console.log(obj_particular, 'part')
  cleaned_common_obj = obj_common.filter(n => n.day == day && n.parking_lot_id == lot)
  cleaned_partic_obj = obj_particular.filter(n => n.day == day && n.parking_lot_id == lot)
    let arr = cleaned_partic_obj[0].hours.reduce((arr, n) => {
    arr.push(n.hour);
    return arr;
  }, []);

  console.log(cleaned_partic_obj.day_id, 'day')

  update_collection.lot = lot;
  update_collection.day_id = cleaned_partic_obj[0].day_id;
  update_collection.original = [...arr];
  update_collection.day = day;
  update_collection.hours = arr;

  let str = '';

  for(let i=0; i<24; i++){
    let d = i < 10 ? '0'+i : i;
    let isDisabled = cleaned_common_obj[0].hours.find(n => n.hour == d && !cleaned_partic_obj[0].hours.find(k=> k.hour == d)) ? 'disabled' : false;
    let isChangable = cleaned_partic_obj[0].hours.find(n => n.hour == d) ? 'checked' : false;
    str += `
      <label class=${isDisabled ? "off_checkbox": ''}>${d}   </label>
      <input type='checkbox' class='update_inp' ${isDisabled} ${isChangable} value=${d}> 
      `
  }
  str += `<input type='submit' id='send_upd'>` 
  elem.innerHTML = str;
  document.querySelectorAll('.update_inp').forEach(n => n.onchange = (e)=> upd_collection_func(e))
  document.querySelector('#send_upd').onclick = send_upd;
}

function send_upd(){
  fetchDataPost(`/update_reservation/`, update_collection);
  window.location.reload(false);
}

function upd_collection_func(event){
  console.log( event.target.value, 'value' )
  let index = update_collection.hours.indexOf(event.target.value);
  if(event.target.checked){
    if(index = -1) update_collection.hours.push(event.target.value)
  }else{
    update_collection.hours.splice(index, 1)
  }
  console.log(update_collection,'collection')
}


function onClickDays(){

  let hours = document.querySelector('#hours'); 
  for(let elem of document.querySelectorAll('.td_class')){
    elem.addEventListener('click', open_booking);

      function open_booking(){
        add_day(hours, document.querySelectorAll('.td_class'), elem); 
        this.removeEventListener('click', open_booking);
        this.addEventListener('click', close_booking);
      }

      function close_booking(){
        remove_day(hours, document.querySelectorAll('.td_class'), elem);
        this.removeEventListener('click', close_booking);
        this.addEventListener('click', open_booking);
      }
  }
  console.log(time_object, 'timeobject')
}

function prev_func(){
  if(cur_month > 0 ){
    cur_month--;
  } else{
    cur_year--;
    cur_month = 11 ;
  }
  createCalendar(document.querySelector('#calendar'), cur_year, cur_month);
};

function next_func(){
  if(cur_month < 11){
    cur_month++;
  } else{
    cur_year++;
    cur_month = 0 ;
  }
  createCalendar(document.querySelector('#calendar'), cur_year, cur_month);
};


function send_info(e){
  fetchDataPost('/book_parking/', time_object)
}

async function fetchDataGet(calendar) {
    try {
      const response = await fetch('/get_all_hours/');
      const json = await response.json();
      booking_info = json.bookings;
      my_bookings = json.filtered;
      console.log(json)
      createCalendar(calendar, cur_year, cur_month);

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


function remove_day(hours, elems, current_elem){
  current_elem.classList.remove('green');
  hours.innerHTML = '';

  let changed_day = time_object[current_elem.dataset.book].filter(n => !arr_temp.includes(n))

  if(time_object[current_elem.dataset.book].length == 0){
    let index = time_object['dates_set'].indexOf(current_elem.dataset.book);
    time_object['dates_set'].splice(index, 1);
  }
  reservation_info(current_elem.dataset.book);
}

function add_day(hours, elems, current_elem){
  hours.innerHTML = '';
  if(current_mode == 'booking'){
    current_elem.classList.add('green');

    let users_hours = booking_info.find(n => n.day == current_elem.dataset.book);
    let new_arr = users_hours ? users_hours.hours.reduce((arr, item) => { 
      arr.push(item.hour)
      return arr;
    }, [])
    : []

    let new_arr_for_adding = arr_temp.filter(n => !new_arr.includes(n));

    time_object[current_elem.dataset.book] = new_arr_for_adding; 
    let index = time_object['dates_set'].indexOf(current_elem.dataset.book);
    if(index == -1) time_object['dates_set'].push(current_elem.dataset.book);
    reservation_info(current_elem.dataset.book);
  } 

  for(let el of elems){
    current_elem == el ?  el.classList.add('active_day') :  el.classList.remove('active_day')
  }
  create_hours_tbl(hours, current_elem.dataset.book, current_elem, time_object['parking_lot']);
}



function add_hour(hour_elem, date){
  hour_elem.classList.add('hours_green');
  time_object[date] ?  time_object[date].push(hour_elem.id) : time_object[date] = [hour_elem.id] ;
  reservation_info(date);
}

function remove_hour(hour_elem, date, parent_day){
  hour_elem.classList.remove('hours_green');

  let index = time_object[date].indexOf(hour_elem.id);
  time_object[date].splice(index, 1);
  
  if(hour_elem.id >= 8 && hour_elem.id <= 17 && parent_day){
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
}

function create_hours_tbl(par, date, parent_day, parking_lot){
  let title = `<h1>${date}</h1>`;
  let hours_tbl = title  + '<table id="hours_t"><tr>';
  for(let i = 0; i < 24; i++){
    let hour_i = i < 10 ? '0'+i : i;
    let busyClass = classTdHour(date, hour_i, parking_lot);
    let classN = i >= 8 && i <= 17 && current_mode == 'booking' ? 'hours_class hours_green' : 'hours_class';
    let show_busy = busyClass ?  busyClass : classN;
      hours_tbl +=`<td id='${hour_i}' class="${show_busy}">${hour_i}:00</td>`
  }
  hours_tbl += '</tr></table>';
  par.insertAdjacentHTML('afterbegin', hours_tbl)
  console.log('ljljljlk')

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

function classTdHour(parent_day, number_h, parking_lot){
  let arr1 = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17' ]
  let users_hours = booking_info.find(n => n.day == parent_day);
  let newClass = users_hours && users_hours.hours.find(n => n.hour == number_h && users_hours.parking_lot_id == parking_lot) ? 'busy_hour' : '';
  return newClass
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
  elem.innerHTML = '';
  let show_month = month+1 < 10 ? '0'+( month+1 ) : month+1;
  let d = new Date(year, month);
  let title = `<h1>${show_month}.${year}</h1>`

  let table = title  +'<table><tr><th>пн</th><th>вт</th><th>ср</th><th>чт</th><th>пт</th><th>сб</th><th>вс</th></tr><tr>';
  for(let i = 0; i < getDay(d); i++)  table += '<td></td>';

  while(d.getMonth() == month){
    table += `<td data-book=${formatDate(d)} class="td_class">` + d.getDate() + '</td>';
    if (getDay(d) % 7 == 6){ table += '</tr><tr>'; }
    d.setDate(d.getDate() + 1);
  }

  if(getDay(d) != 0){
    for (let i = getDay(d); i < 7; i++){
      table += '<td></td>';
    }
  }

  table += '</tr></table>';
  elem.innerHTML = table;

  document.getElementById('prev').onclick = prev_func;
  document.getElementById('next').onclick = next_func;
  onClickDays()
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


