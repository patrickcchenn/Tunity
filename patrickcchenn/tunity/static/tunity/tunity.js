document.addEventListener('DOMContentLoaded', function () {
  

  document.querySelectorAll('.accept_button').forEach((button) => {
    button.onclick = function () {
      let user= this.dataset.user;
      let vacancy_id= this.dataset.vacancy;
      

      fetch(`/update/${user}/${vacancy_id}`, {
        method: 'POST',
        body: JSON.stringify({
          user: `${user}`,
          vacancy_id: `${vacancy_id}`,
          condition: true,
        }),
      });
      
      
      document.querySelector(`#accept_${user}-${vacancy_id}`).style.display =
        'none';
      document.querySelector(`#decline_${user}-${vacancy_id}`).style.display =
        'none';
      document.querySelector('#message').innerHTML='Accepted!';
    };
  });

  document.querySelectorAll('.decline_button').forEach((button) => {
    button.onclick = function () {
      let user= this.dataset.user;
      let vacancy_id= this.dataset.vacancy;

      fetch(`/update/${user}/${vacancy_id}`, {
        method: 'POST',
        body: JSON.stringify({
          user: `${user}`,
          vacancy_id: `${vacancy_id}`,
          condition: false,
        }),
      });
      // PROBLEM HERE
      document.querySelector(`#accept_${user}-${vacancy_id}`).style.display =
        'none';
      document.querySelector(`#decline_${user}-${vacancy_id}`).style.display =
        'none';
      document.querySelector('#message').innerHTML='Declined';

    };
  });
});
