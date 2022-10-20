const trainingUrl = document.querySelector('#training-url')
const faceIdentification = document.querySelector('#face-identification')
const modal = document.getElementById("myModal");
function Alertgreen() {
  const alert = document.querySelector(".alert-green");
  const closebtn = document.querySelector(".close-btn-green");
  alert.classList.add("show");
  alert.classList.remove("hide");
  alert.classList.add("showAlert");
  alert.style.display = "block";
  setTimeout(function () {
    alert.classList.remove("show");
    alert.classList.add("hide");
    setTimeout(function () {
      alert.style.display = "none";
    }, 1000);
  }, 1000);
  closebtn.onclick = () => {
    alert.classList.remove("show");
    alert.classList.add("hide");
    setTimeout(function () {
      alert.style.display = "none";
    }, 1000);
  };
}
function Alertred() {
  const alert = document.querySelector(".alert-red");
  const closebtn = document.querySelector(".close-btn-red");
  alert.classList.add("show");
  alert.classList.remove("hide");
  alert.classList.add("showAlert");
  alert.style.display = "block";
  setTimeout(function () {
    alert.classList.remove("show");
    alert.classList.add("hide");
    etTimeout(function () {
      alert.style.display = "none";
    }, 1000);
  }, 3000);
  closebtn.onclick = () => {
    alert.classList.remove("show");
    alert.classList.add("hide");
    etTimeout(function () {
      alert.style.display = "none";
    }, 1000);
  };
}

trainingUrl.onclick = () => {
    console.log("TRAINING CLICKING")
    modal.style.display = "block";
    callTrainingAPI()
}

async function callTrainingAPI(){
    const config = {
        method: 'PUT',
        url: '/home/training/',
    };
      
    axios(config)
    .then(function (response) {
        modal.style.display = "none";
        Alertgreen()
        console.log(JSON.stringify(response.data));
    })
    .catch(function (error) {
        Alertred()
        console.log(error);
        console.log(error.response);
        console.log(error.response.data);
    });
}

faceIdentification.onclick = () => {
    console.log("FACE IDENTIFICATION CLICKING")
    callFaceIDAPI()
}

async function callFaceIDAPI(){
    const config = {
        method: 'PUT',
        url: '/faceidentifier/',
    };
      
    axios(config)
    .then(function (response) {
        console.log(JSON.stringify(response.data));
    })
    .catch(function (error) {
        console.log(error);
        console.log(error.response);
        console.log(error.response.data);
    });
}
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
    
  }
};