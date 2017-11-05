/**
 * Created by liuziqi on 2017/9/3.
 */
$.backstretch([
    "/static/img/backgrounds/a.jpg"
    , "/static/img/backgrounds/b.jpg"
    , "/static/img/backgrounds/c.jpg"
], {duration: 3000, fade: 750});


function check_signup() {
    var username = $('#username');
    var pw1 = $('#password');
    var pw2 = $('#confirm-password');
    var email = $('#email');
    var re1 = /[a-zA-Z0-9]{6,128}/;
    if (!re1.test(username.value)) {
        alert('username must be 6-128 letters or numbers');
        return false;
    }
    if (pw1.value.length < 6) {
        alert('password must be more than 6 characters!');
        return false;
    }
    if (pw1.value !== pw2.value) {
        alert("two password don't match!");
        return false;
    }
    var re2 = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
    if (!re2.test(email.value)) {
        alert(email.value);
        alert('illegal email!');
        return false;
    }
    return true;
}