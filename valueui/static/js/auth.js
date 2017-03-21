function postRegistrationForm(form)
{
  $.ajax({
    url: '/api/register',
    method: "POST",
    data: form.serialize(),
  })
    .then( function (data) {
      data = JSON.parse(data)
      console.log(data)
      if(data['code'][0] === 'REGISTER_SUCCESS')
      {
	document.location.href = '/login';
      }
    })
    .fail(function(error){
      console.log("Registration failed: " + error)
    });
}

function postLoginForm(form)
{
  $.ajax({
    url: '/api/login',
    method: "POST",
    data: form.serialize(),
  }).done( function (data) {
    data = JSON.parse(data)
    setupAjax(data['csrf'])
    console.log(data)
    if(data['code'][0] === 'LOGIN_SUCCESS')
    {
      document.location.href = '/';
    }
  });
}

function sendLogout()
{
  $.ajax({
    url: '/api/logout',
    method: "GET",
  }).done( function (data) {
    data = JSON.parse(data)
    setupAjax(data['csrf'])
    console.log(data)
    if(data['code'][0] === 'LOGOUT_SUCCESS')
    {
      document.location.href = '/';
    }	
  });
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function setupAjax(csrf_token)
{
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	xhr.setRequestHeader("X-CSRFToken", csrf_token);
      }
    }
  });
}
