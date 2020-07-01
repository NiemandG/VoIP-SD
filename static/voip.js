const query_phone = 'RouterCallKeyDay,RouterCallKey,DateTime,DigitsDialed,CED,Duration,TalkTime,Variable1,Variable3,Variable4,Variable7,Variable8, Variable9, Variable10,DNIS,ANI,InstrumentPortNumber,AgentPeripheralNumber,SkillGroupSkillTargetID';
let b1 = document.getElementById("b1");
let b2 = document.getElementById("b2");
let b3 = document.getElementById("b3");
let b4 = document.getElementById("b4");
let b5 = document.getElementById("b5");
let b6 = document.getElementById("b6");
let b7 = document.getElementById("b7");
let b8 = document.getElementById("b8");
let b9 = document.getElementById("b9");
let c1 = document.getElementById("c1");
let c2 = document.getElementById("c2");
let c3 = document.getElementById("c3");
let c4 = document.getElementById("c4");
let c5 = document.getElementById("c5");
let c6 = document.getElementById("c6");
let c7 = document.getElementById("c7");
let c8 = document.getElementById("c8");
let c9 = document.getElementById("c9");




copy = function(x) {
    let range = document.createRange();
    range.selectNode(x);
    document.getSelection().removeAllRanges();
    document.getSelection().addRange(range);
    let successful = document.execCommand('copy');
    let stg = successful ? 'successful' : 'unsuccessful';
    console.log("Скопированный текст: " + stg);
    document.getSelection().removeAllRanges();
}
b1.addEventListener("click", function() {
    copy(c1);
}, false);
b2.addEventListener("click", function() {
    copy(c2);
}, false);
b3.addEventListener("click", function() {
    copy(c3);
}, false);
b4.addEventListener("click", function() {
    copy(c4);
}, false);
b5.addEventListener("click", function() {
    copy(c5);
}, false);
b6.addEventListener("click", function() {
    copy(c6);
}, false);
b7.addEventListener("click", function() {
    copy(c7);
}, false);
b8.addEventListener("click", function() {
    copy(c8);
}, false);
b9.addEventListener("click", function() {
    copy(c9);
}, false);

exist_finesse_1.oninput = function() {
    exist_finesse_start.innerHTML = this.value;
    range_begin.innerHTML = this.value[0];
}
exist_finesse_2.oninput = function() {
    exist_finesse_end.innerHTML = this.value;
}
unuse_finesse_1.oninput = function() {
    unuse_begin.innerHTML = this.value;
}
unuse_finesse_2.oninput = function() {
    unuse_end.innerHTML = this.value;
}
unusealt_finesse_1.oninput = function() {
    unusealt_begin.innerHTML = this.value;
}
unusealt_finesse_2.oninput = function() {
    unusealt_end.innerHTML = this.value;
}

select_all.oninput = function() {
    query1.innerHTML = '*';

}
select_main.oninput = function() {
    query1.innerHTML = query_phone;
}
phone1.oninput = function() {
    let phone = this.value.trim()

    if ((phone.length > 10) && (phone.length < 12)) {
        phone = phone.slice(1);
        console.log(phone);
        phone_for_search_1.innerHTML = phone;
        phone_for_search_2.innerHTML = phone;
        phone_for_search_3.innerHTML = phone;
    } else if (phone.length === 10) {
        console.log(phone);
        phone_for_search_1.innerHTML = phone;
        phone_for_search_2.innerHTML = phone;
        phone_for_search_3.innerHTML = phone;
    } else if (phone.length > 11) {
        alert("Неверный формат телефона");
    }
}
RCK.oninput = function() {
    rck_val.innerHTML = this.value;
    rck_onoff.innerHTML = "";
    phone_onoff.innerHTML = "--";
    if (this.value.length === 0) {
        rck_onoff.innerHTML = "--";
        phone_onoff.innerHTML = "";
    }
}
RCKD.oninput = function() {
    rckd_val.innerHTML = this.value;
    rckd_onoff.innerHTML = "";
    date_onoff.innerHTML = "--";
    phone_onoff.innerHTML = "--"
    if (this.value.length === 0) {
        rckd_onoff.innerHTML = "--";
        date_onoff.innerHTML = "";
        phone_onoff.innerHTML = ""
    }
}
phone_date_begin.oninput = function() {
    let x = this.value;
    datebegin.innerHTML = this.value;
    console.log(x);
}
phone_date_end.oninput = function() {
    dateend.innerHTML = this.value;

}