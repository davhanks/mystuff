function myFunction()
    {

    var r=confirm("Pressing OK will create a new store with a unique ID. Are you sure?");
    if (r==true)
      {
        window.location = "/manager/editstore/new/";
      }
    else
      {
        window.location = "/manager/storelist/";
      }

    }

function showConfirm() {
  document.getElementById('confirmation').style.visibility = 'visible';
}

function hideConfirm() {
  document.getElementById('confirmation').style.visibility = 'hidden';
}

function showLogout() {
  document.getElementById('logout').style.visibility = 'visible';
}

function hideLogout() {
  document.getElementById('logout').style.visibility = 'hidden';
}