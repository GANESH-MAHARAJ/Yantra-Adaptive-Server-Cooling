const acc1 = {
  owner: 'Abhinav Kenguva',
  username: 'abhi123',
  password: 'abhi@123',
};

const acc2 = {
  owner: 'Ganesh Maharaj',
  username: 'ganesh123',
  password: 'ganesh@123',
};

const acc3 = {
  owner: 'admin',
  username: 'admin',
  password: '1234',
};

const accounts = [acc1, acc2, acc3];

const btnLogin = document.querySelector('.button');
const inputUsername = document.getElementById('username');
const inputPassword = document.getElementById('password');

btnLogin.addEventListener('click', function (e) {
  e.preventDefault();

  const acc = accounts.find(x => x.username === inputUsername.value);

  if (acc && acc.password === inputPassword.value) {
    inputPassword.value = inputUsername.value = '';
    inputPassword.blur();
    inputUsername.blur();

    window.location.href = 'main.html';
  } else {
    alert('Invalid credentials');
  }
});
